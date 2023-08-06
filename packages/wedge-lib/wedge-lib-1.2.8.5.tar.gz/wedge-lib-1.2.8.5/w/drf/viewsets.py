from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from w import exceptions
from w.services.abstract_model_service import AbstractModelService


class ViewSet(viewsets.ViewSet):
    serializers = {"default": None}

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_key = kwargs.pop("serializer_key", None)
        serializer_class = self.get_serializer_class(serializer_key)
        return serializer_class(*args, **kwargs)

    @classmethod
    def get_serializer_by_key(cls, key):
        """
        Args:
            key: serializer key

        Returns:
            Serializer
        """
        return cls.serializers.get(key, cls.serializers["default"])

    def get_serializer_class(self, serializer_key=None):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)

        Returns:
            Serializer: Drf or Serpy
        """
        serializer_key = serializer_key if serializer_key else self.action  # noqa
        return self.get_serializer_by_key(serializer_key)

    def get_action(self):
        # noinspection PyUnresolvedReferences
        return self.action_map.get(self.request.method.lower())

    def get_response(self, data, **params) -> Response:
        """
        Get response from data.

        Automatically serialize data from action name or parameter serializer_key

        Args:
            data(mixed): data to return in response
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_200_OK

        Returns:
            Response
        """
        default = {
            "serializer_key": None,
            "status_code": status.HTTP_200_OK,
        }
        params = {**default, **params}
        serializer_class = self.get_serializer_class(params["serializer_key"])
        many = isinstance(data, list)
        serializer = serializer_class(data, many=many)

        return Response(serializer.data, status=params.get("status_code"))

    def get_post_response(self, data, **params) -> Response:
        """
        Get post response from data.

        Automatically serialize data from action name or parameter serializer_key

        Args:
            data(mixed): data to return in response
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_201_CREATED
        Returns:
            Response
        """
        default = {
            "serializer_key": None,
            "status_code": status.HTTP_201_CREATED,
        }
        params = {**default, **params}
        return self.get_response(data, **params)

    def get_validated_data(self, serializer_key=None):
        """
        Validate request data (throw exception if invalid) and return validated data

        Args:
            serializer_key(None|str): serializer to use,
                default is "<action name>_validation"

        Returns:
            dict
        """
        if serializer_key is None:
            serializer_key = f"{self.action}_validation"
        if serializer_key not in self.serializers:
            raise RuntimeError(f"You need to define '{serializer_key}' serializer")
        serializer_class = self.get_serializer_class(serializer_key)
        serializer = serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @classmethod
    def _simplify_errors(cls, errors):
        if isinstance(errors, dict):
            return {attr: cls._simplify_errors(errs) for attr, errs in errors.items()}
        if isinstance(errors, list) and isinstance(errors[0], dict):
            # Simplify many to many relations errors
            many2many_errors = []
            for item_errors in errors:
                many2many_errors.append(cls._simplify_errors(item_errors))
            return many2many_errors
        return str(errors[0])

    @staticmethod
    def get_error_validation_response(error: ValidationError):
        """
        Build validation error response with status code of 422 and
        by keeping only first validation message
        """
        data = {}
        for attr, errors in error.detail.items():
            data[attr] = str(errors[0])
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def check_is_valid(self, serializer_key=None):
        try:
            validated_data = self.get_validated_data(serializer_key)
        except ValidationError as e:
            errors = self._simplify_errors(e.detail)
            raise exceptions.ValidationError(errors)
        return dict(validated_data)

    @action(methods=["post"], detail=False)
    def validate(self, request):
        """
        Validate using query params action to retrieve serializer name

        POST <viewset>/validate/?action=<action name>
        """
        action_name = self.request.GET.get("action")
        if action_name is None:
            raise RuntimeError("missing query parameter 'action'")
        validated_data = self.check_is_valid(serializer_key=f"{action_name}_validation")
        return Response(validated_data)


class ModelServiceViewSet(ViewSet):
    service: AbstractModelService

    def get_detail_response(
        self, instance=None, serializer_key=None, status_code=status.HTTP_200_OK
    ) -> Response:
        """
        Build response

        Args:
            instance(Model|None): if None use service.get_by_pk
            serializer_key: default: None,
            status_code: default: status.HTTP_200_OK

        Returns:

        """
        if instance is None:
            instance = self.service.check_by_pk(self.kwargs["pk"])
        serializer_class = self.get_serializer_class(serializer_key)
        return Response(serializer_class(instance).data, status=status_code)

    def get_list_response(self, queryset=None, **params):

        """
        Get post response from data.

        Automatically serialize data from action name or parameter serializer_key.

        if data is empty build response from

        Args:
            queryset(QuerySet): data to return in response
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_201_CREATED
        Returns:
            Response
        """
        default = {
            "serializer_key": None,
            "status_code": status.HTTP_200_OK,
        }
        params = {**default, **params}

        serializer_class = self.get_serializer_class(params.get("serializer_key"))
        if queryset is None:
            queryset = self.service.list()

        optimized_queryset = serializer_class.get_optimized_queryset(queryset)
        if self.request.query_params:
            optimized_queryset = optimized_queryset.filter(
                **self.request.query_params.dict()
            )
        serializer = serializer_class(optimized_queryset, many=True)
        return Response(serializer.data, params.get("status_code"))

    def get_retrieve_response(self, instance=None, **params) -> Response:
        """
        Build retrieve response
        Args:
            instance(Model|None): if None use service.get_by_pk
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_201_CREATED

        Returns:
            Response
        """
        return self.get_detail_response(instance=instance, **params)

    def get_create_response(self, instance, **params) -> Response:
        """
        Build create response

        Args:
            instance(Model): model instance created
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_201_CREATED

        Returns:
            Response
        """
        default = {"status_code": status.HTTP_201_CREATED}
        params = {**default, **params}
        return self.get_detail_response(instance=instance, **params)

    def get_update_response(self, instance, **params) -> Response:
        """
        Build update response
        Args:
            instance(Model): model instance updated
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_200_OK

        Returns:
            Response
        """
        return self.get_detail_response(instance=instance, **params)

    def get_delete_response(self, instance=None, **params) -> Response:
        """
        Build delete response. If instance is None => Response status=204

        Args:
            instance(Model|None): model instance deleted
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_200_OK ou HTTP_204_NO_CONTENT si
                                instance is None

        Returns:
            Response
        """
        if instance:
            return self.get_detail_response(instance=instance, **params)
        return Response(status=status.HTTP_204_NO_CONTENT)
