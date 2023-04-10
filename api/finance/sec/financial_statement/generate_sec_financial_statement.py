import api.finance.sec.financial_statement.raw_data as afsfsrd
import api.finance.sec.financial_statement.preprocess.original_cik_data as afsfspocd
import api.finance.sec.financial_statement.preprocess.modified_cik_data as afsfspmcd


afsfsrd.prepare_sec_raw_data()
afsfspocd.get_original_cik_data()
afsfspmcd.generate_all_unified_attribute_financial_statement()
