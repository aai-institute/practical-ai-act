from pathlib import Path

from sensai import InputOutputData
from ucimlrepo import fetch_ucirepo
from sensai.util.cache import pickle_cached


COL_STATUS_EXISTING_ACCOUNT = "status_existing_account"
COL_DURATION = "duration"
COL_CREDIT_HISTORY = "credit_history"
COL_PURPOSE = "purpose"
COL_CREDIT_AMOUNT = "credit_amount"
COL_SAVINGS = "savings"
COL_EMPLOYMENT_SINCE = "employment_since"
COL_INSTALLMENT_RATE = "installment_rate"
COL_PERSONAL_STATUS = "personal_status"
COL_OTHER_DEBTORS = "other_debtors"
COL_RESIDENCE_SINCE = "residence_since"
COL_PROPERTY = "property"
COL_AGE = "age"
COL_OTHER_INSTALLMENT_PLANS = "other_installment_plans"
COL_HOUSING = "housing"
COL_NUMBER_EXISTING_CREDITS = "number_existing_credits"
COL_JOB = "job"
COL_NUMBER_PEOPLE_LIABLE = "number_people_liable"
COL_TELEPHONE = "telephone"
COL_FOREIGN_WORKER = "foreign_worker"
COL_CLASSIFICATION = "class"

COLS_ALL = (
    COL_STATUS_EXISTING_ACCOUNT,
    COL_DURATION,
    COL_CREDIT_HISTORY,
    COL_PURPOSE,
    COL_CREDIT_AMOUNT,
    COL_SAVINGS,
    COL_EMPLOYMENT_SINCE,
    COL_INSTALLMENT_RATE,
    COL_PERSONAL_STATUS,
    COL_OTHER_DEBTORS,
    COL_RESIDENCE_SINCE,
    COL_PROPERTY,
    COL_AGE,
    COL_OTHER_INSTALLMENT_PLANS,
    COL_HOUSING,
    COL_NUMBER_EXISTING_CREDITS,
    COL_JOB,
    COL_NUMBER_PEOPLE_LIABLE,
    COL_TELEPHONE,
    COL_FOREIGN_WORKER,
    COL_CLASSIFICATION,
)

COL_TARGET = COL_CLASSIFICATION

COLS_FEATURE_ALL = tuple([col for col in COLS_ALL if col != COL_TARGET])
COLS_FEATURE_NUMERIC = (COL_DURATION, COL_CREDIT_AMOUNT, COL_INSTALLMENT_RATE, COL_RESIDENCE_SINCE, COL_AGE, COL_NUMBER_EXISTING_CREDITS, COL_NUMBER_PEOPLE_LIABLE)
COLS_FEATURE_CATEGORICAL = tuple([col for col in COLS_FEATURE_ALL if col not in COLS_FEATURE_NUMERIC])


class StatLogData:

    def __init__(self, data_path: str | Path | None = None):
        self._data_path = data_path

        loading_func = fetch_ucirepo

        if data_path is not None:
            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(id=144)


    def load_data_frame(self):
        column_renaming_dict = dict(zip(self._data.data.original.columns, COLS_ALL))
        return self._data.data.original.rename(columns=column_renaming_dict)

    def load_input_output_data(self):
        all_df = self.load_data_frame()
        return InputOutputData(all_df.drop(columns=[COL_TARGET]), all_df[[COL_TARGET]])