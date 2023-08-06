import pytest
from openpyxl import Workbook

from w.services.technical.excel_service import ExcelService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestExcelService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.filename = cls.get_datasets_dir("excel/Excel2010.xlsx")
        cls.mapping = {"header1": "columnA", "header2": "columnB", "header3": "columnC"}

    """
    is_excel
    """

    def test_is_excel_with_no_excel_file_return_false(self):
        """ Ensure method return False on no excel file """
        files = ["toto.txt", "excel.txt", "excel.xls.gz"]
        for file in files:
            assert ExcelService.is_excel(file) is False

    def test_is_excel_with_success_return_true(self):
        """ Ensure method return True on excel file """
        files = ["toto.xls", "excel.xlsx"]
        for file in files:
            assert ExcelService.is_excel(file) is True

    """
    open_workbook
    """

    def test_open_workbook_with_file_not_exists_raise_runtime_error(self):
        """ Ensure RuntimeError is raised if filename does not exists """
        with pytest.raises(RuntimeError, match="unknown-file does not exists"):
            ExcelService.open_workbook("unknown-file")

    def test_open_workbook_with_invalid_excel_suffix_raise_runtime_error(self):
        """ Ensure method raise runtime error if file is not excel """
        filename = self.get_datasets_dir("csv/simple.csv")
        match = "simple.csv is not a valid excel file"
        with pytest.raises(RuntimeError, match=match):
            ExcelService.open_workbook(filename)

    def test_open_workbook_with_not_valid_excel_raise_runtime_error(self):
        """ Ensure RuntimeError is raised if filename is not valid excel """
        filename = self.get_datasets_dir("excel/invalid_excel.xls")
        match = "invalid_excel.xls is not a valid excel file"
        with pytest.raises(RuntimeError, match=match):
            ExcelService.open_workbook(filename)

    def test_open_workbook_with_success_return_book(self):
        """ Ensure method succeed return Book """
        actual = ExcelService.open_workbook(self.filename)
        assert isinstance(actual, Workbook)

    """
    load
    """

    def test_load_with_invalid_excel_suffix_raise_runtime_error(self):
        """ Ensure method raise runtime error if file is not excel """
        filename = self.get_datasets_dir("csv/simple.csv")
        match = "simple.csv is not a valid excel file"
        with pytest.raises(RuntimeError, match=match):
            ExcelService.load(filename, self.mapping)

    def test_load_with_not_valid_excel_raise_runtime_error(self):
        """ Ensure RuntimeError is raised if filename is not valid excel """
        filename = self.get_datasets_dir("excel/invalid_excel.xls")
        match = "invalid_excel.xls is not a valid excel file"
        with pytest.raises(RuntimeError, match=match):
            ExcelService.load(filename, self.mapping)

    def test_load_with_invalid_header_raise_runtime_error(self):
        """ Ensure method raise runtime error if header is false """
        mapping = self.mapping.copy()
        mapping["colWrong"] = mapping.pop("header3")
        match = (
            "incorrect or missing header, expected 'header1, header2, colWrong'"
            " got 'header1, header2, header3'"
        )
        with pytest.raises(RuntimeError, match=match):
            ExcelService.load(self.filename, mapping)

    def test_load_with_success_return_list(self):
        """ Ensure method succeed """
        self.assert_equals_resultset(ExcelService.load(self.filename, self.mapping))

    def test_load_with_specific_bad_sheet_name_raise_runtime_error(self):
        """ Ensure method raise runtime error if sheet name is bad """
        match = "bad_sheet_name is not a valid sheet name"

        with pytest.raises(RuntimeError, match=match):
            ExcelService.load(self.filename, self.mapping, "bad_sheet_name")

    def test_load_with_specific_sheet_name_success_return_list(self):
        """ Ensure method succeed with specific sheet name """
        mapping = {
            "header1_sheet2": "columnA",
            "header2_sheet2": "columnB",
            "header3_sheet2_with_space": "columnC",
        }

        self.assert_equals_resultset(
            ExcelService.load(self.filename, mapping, "Sheet_2")
        )
