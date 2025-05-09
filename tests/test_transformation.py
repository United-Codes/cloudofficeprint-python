import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop

def test_initialization_with_js_code():
    tf = cop.TransformationFunction(js_code="function() {}")
    expected = "function() {}"
    assert tf.js_code == expected
    assert tf.as_dict() == expected

def test_initialization_with_filename():
    tf = cop.TransformationFunction(filename="test.js")
    assert tf.as_dict() == "test.js"

def test_initialization_with_both_raises_error():
    error_occurred = False
    try:
        cop.TransformationFunction(js_code="code", filename="test.js")
    except ValueError as e:
        error_occurred = True
        assert "Cannot set filename when js_code is already set" in str(e)  
    assert error_occurred

def test_filename_path_validation():
    error_occurred = False
    try:
        cop.TransformationFunction(filename="invalid/path/test.js")
    except ValueError as e:
        error_occurred = True
        assert "must not include any path separators" in str(e)  
    assert error_occurred

def test_mutually_exclusive_properties():
    tf = cop.TransformationFunction(js_code="code")
    error_occurred = False
    try:
        tf.filename = "new.js"
    except ValueError as e:
        error_occurred = True
        assert "Cannot set filename" in str(e)
    assert error_occurred

def test_as_dict_with_neither():
    tf = cop.TransformationFunction()
    assert tf.as_dict() is None

def run():
    test_initialization_with_js_code()
    test_initialization_with_filename()
    test_initialization_with_both_raises_error()
    test_filename_path_validation()
    test_mutually_exclusive_properties()
    test_as_dict_with_neither()

if __name__ == "__main__":
    run()