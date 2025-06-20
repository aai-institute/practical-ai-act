def test_definitions():
    """Assert that the Dagster definitions can be loaded without errors"""

    from income_prediction import definitions

    assert definitions
    assert definitions.get_job_def("e2e_pipeline_job")
