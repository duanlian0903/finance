import api.finance.sec.financial_statement.raw_data as afsfsrd
import api.finance.sec.financial_statement.preprocess.original_cik_data as afsfspocd
import api.finance.sec.financial_statement.preprocess.unified_attribute_cik_data as afsfspuacd


afsfsrd.prepare_sec_raw_data()
afsfspocd.get_original_cik_data()
afsfspuacd.generate_all_unified_attribute_financial_statement()
