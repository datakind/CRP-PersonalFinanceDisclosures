import pandas as pd
import numpy as np
import codecs

# transactions_income = pd.read_csv('Goal2_PFD_Assets_Transactions_Income.csv', encoding='ISO-8859-1', low_memory=False)

pdf_assets_headers = ['ID', 'Chamber', 'CID', 'CalendarYear', 'ReportType', 'SenAB',
'AssetSpouseJointDep', 'AssetSource', 'Orgname','Ultorg', 'RealCode','Source', 'AssetDescrip', 'Orgname2',
'Ultorg2', 'RealCode2' ,'Source2', 'AssetSourceLocation', 'AssetValue', 'AssetExactValue',
'AssetDividends AssetRent AssetInterest AssetCapitalGains AssetExemptedFund',
'AssetExemptedTrust AssetQualifiedBlindTrust AssetTypeCRP', 'OtherTypeIncome AssetIncomeAmtRange',
'AssetIncomeAmountText', 'AssetIncomeAmt AssetPurchased AssetSold', 'AssetExchanged Date', 'DateText AssetNotes',
'Dupe', '1','2','3','4','5','6','7','8','9','10', '11']

pdf_trans_headers = ['ID', 'Chamber', 'CID', 'CalendarYear', 'ReportType', 'Asset4SJD',
'Asset4Transacted', 'Orgname', 'Ultorg', 'RealCode',
'Source','Asset4Descrip', 'Orgname2', 'Ultorg2', 'RealCode2',
'Source2', 'Asset4Purchased', 'Asset4Sold',
'Asset4Exchanged', 'Asset4Date', 'Asset4DateText','Asset4TransAmt', 'Asset4ExactAmt', 'CofD', 'TransNotes', 'Dupe']


LU_asset_value = pd.DataFrame({'Chamber': ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'H', 'H', 'H',
                                           'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'J', 'J', 'J', 'J', 'J',
                                           'J', 'J', 'J', 'J', 'J', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
                                           'S', 'S'],
                               'AssetValue': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'A', 'B', 'C', 'D',
                                        'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'J', 'K', 'L', 'M', 'N', 'O', 'P1',
                                        'P2', 'P3', 'P4', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
                               'Lower_Value': [0, 1001, 15001, 50001, 100001, 250001, 500001, 1000001, 1000001, 5000001,
                                               25000001, 50000001, 0, 1, 1001, 15001, 50001, 100001, 250001, 500001,
                                               1000001, 5000001, 25000001, 50000001, 1000001, 0, 15001, 50001, 100001,
                                               250001, 500001, 1000001, 5000001, 25000001, 50000001, 0, 1001, 15001,
                                               50001, 100001, 250001, 500001, 1000001, 1000001, 5000001, 25000001,
                                               50000001],
                               'Upper_Value': [1000, 15000, 50000, 100000, 250000, 500000, 1000000, 1000001, 5000000,
                                               25000000, 50000000, 50000001, 0, 1000, 15000, 50000, 100000, 250000,
                                               500000, 1000000, 5000000, 25000000, 50000000, 50000001, 1000001, 15000,
                                               50000, 100000, 250000, 500000, 1000000, 5000000, 25000000, 50000000,
                                               50000001, 1000, 15000, 50000, 100000, 250000, 500000, 1000000, 1000001,
                                               5000000, 25000000, 50000000, 50000001]})

pdf_assets_converters = {'Chamber': lambda x: x.strip(),
                         'AssetValue': lambda x: str(x).strip()}

pdf_assets_dtypes = {'CalendarYear': int}

pdf_assets = pd.read_csv('PDFAssets.txt', encoding='ISO-8859-1', low_memory=False, quotechar='|',error_bad_lines=False,
                         sep=",",
                         converters=pdf_assets_converters,
                         dtype=pdf_assets_dtypes)
pdf_assets.columns = pdf_assets_headers
pdf_assets['AssetValue'] = pdf_assets['AssetValue'].apply(str).apply(lambda x: x.strip())
print(len(pdf_assets))

"""Fill NaNs"""
pdf_assets.loc[:, ['AssetSpouseJointDep']].fillna('O', inplace=True)


print(pdf_assets.isnull().sum())

"""Drop NA Rows for essentail columns"""
pdf_assets.dropna(axis=0, how='any', inplace=True,
                  subset=['ID', 'Chamber', 'CID', 'CalendarYear', 'ReportType',
                          'AssetSource', 'AssetValue'])
print(len(pdf_assets))

"""Map AssetValue Codes"""
pdf_assets = pdf_assets.merge(LU_asset_value, how="left", on=['Chamber', 'AssetValue'])

"""Consolidate Asset Source Information"""
pdf_assets.loc[:, "AssetName"] = pdf_assets.loc[:, "AssetDescrip"]
print(pdf_assets.loc[:, "AssetName"].isnull().sum())
pdf_assets.loc[:, "AssetName"].fillna(pdf_assets.loc[:, "AssetSource"], inplace=True)
print(pdf_assets.loc[:, "AssetName"].isnull().sum())

"""Correct ReportType"""
pdf_assets.loc[pdf_assets['ReportType'] == 'H',['ReportType']] = 'N'


"""Create table with only the most recent disclosure per year"""


report_order = pd.DataFrame({'ReportType': ['N', 'C', 'O', 'Y', 'A', 'T'],
                             'Report_Order': [1, 2, 3, 4, 5, 6]})
pdf_assets = pdf_assets.merge(report_order, on=['ReportType'])
min_report = pdf_assets.groupby(['CID', 'CalendarYear'])["Report_Order"].agg(min).reset_index()
pdf_assets_final = pdf_assets.merge(min_report, on=['CID', 'CalendarYear', 'Report_Order'], how='inner')


"""CID Aggregate Infromation"""
CID_groupby = pdf_assets_final.groupby(['CID', 'Chamber', 'CalendarYear'])
assets_by_year = CID_groupby['AssetExactValue'].agg(sum).reset_index()
asset_group_by_year = CID_groupby['Upper_Value', 'Lower_Value'].agg(sum).reset_index()
print(assets_by_year[assets_by_year['AssetExactValue'] > 100000000].dropna())

"""Rich Senators"""
print(asset_group_by_year[
          (asset_group_by_year['CalendarYear'] == 12) &
          (asset_group_by_year['Chamber'] == 'S') &
          (asset_group_by_year['Lower_Value'] > 10000000)])

"""Financial Disclosure Scorecard"""



# TODO: Ease of asset identification

# TODO: Exact Asset Values?

#

