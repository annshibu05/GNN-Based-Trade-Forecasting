# # import pandas as pd

# # path = "data/raw/comtrade/TradeData.csv"

# # for enc in ["latin1", "ISO-8859-1", "cp1252"]:
# #     try:
# #         print(f"\nTrying encoding: {enc}")
# #         df = pd.read_csv(path, encoding=enc, low_memory=False)
# #         print(f"Loaded successfully with encoding: {enc}")
# #         print(df.columns)
# #         df.head(3).T
        
# #         print("Unique flowCode:", df['flowCode'].unique())
# #         print("Unique flowDesc:", df['flowDesc'].unique()[:20])
# #         print("Export rows:", (df['flowCode'] == 'Export').sum())
# #         print("Import rows:", (df['flowCode'] == 'Import').sum())
        
# #         print("Reporters:", df['reporterISO'].unique()[:20])
# #         print("Partners:", df['partnerISO'].unique()[:20])

# #         print(df.head())
# #         break
# #     except Exception as e:
# #         print(f"Failed with {enc}: {e}")

# import pandas as pd

# for enc in ['utf-8', 'latin1', 'cp1252', 'windows-1252', 'ISO-8859-1']:
#     try:
#         print("Trying:", enc)
#         df = pd.read_csv("data/raw/comtrade/TradeData.csv", encoding=enc)
#         print("flowDesc sample:", df['flowDesc'].head())
#     except Exception as e:
#         print("Failed:", enc, e)


import pandas as pd
df = pd.read_csv("data/raw/comtrade/TradeData.csv", encoding="latin1", low_memory=False)

print("rows, cols:", df.shape)
print("reporterISO unique sample:", pd.Series(df['reporterISO'].unique()).head(20).tolist())
print("reporterDesc unique sample:", pd.Series(df['reporterDesc'].unique()).head(20).tolist())
print("flowCode unique:", df['flowCode'].unique())
print("flowDesc unique:", pd.Series(df['flowDesc'].unique()).head(20).tolist())
print("cmdCode sample values:", pd.Series(df['cmdCode'].unique()).head(20).tolist())
print("Does primaryValue column exist? ->", 'primaryValue' in df.columns)
print("primaryValue dtype:", df['primaryValue'].dtype)

# A: reporterISO equals 'IND' (exact match)
print("Exact reporterISO == 'IND':", len(df[df['reporterISO'] == 'IND']))

# B: reporterISO contains 'IND' (case-insensitive)
print("reporterISO contains 'IND':", len(df[df['reporterISO'].astype(str).str.upper().str.contains('IND', na=False)]))

# C: reporterDesc contains 'India'
print("reporterDesc contains 'India':", len(df[df['reporterDesc'].astype(str).str.contains('India', case=False, na=False)]))

# D: any India rows regardless of flow
india_any = df[df['reporterISO'].astype(str).str.upper().str.contains('IND', na=False) |
               df['reporterDesc'].astype(str).str.contains('India', case=False, na=False)]
print("india_any rows:", len(india_any))
print(india_any[['reporterISO','reporterDesc','flowCode','flowDesc','primaryValue']].head(10).to_string(index=False))


india = india_any.copy()
print("Unique flowCode for India:", india['flowCode'].unique())
print("Unique flowDesc for India (sample):", pd.Series(india['flowDesc'].unique()).tolist()[:10])


# show primaryValue raw values for first India rows
print(india_any[['primaryValue']].head(20).to_string(index=False))

# show if there are commas or non-numeric chars
sample = india_any['primaryValue'].astype(str).head(50).tolist()
print("sample primaryValue strings:", sample)



# find India rows where primaryValue seems > 0 after coercion
india_any['primary_num'] = pd.to_numeric(india_any['primaryValue'].astype(str).str.replace(',',''), errors='coerce')
print("India rows with primary_num >0:", len(india_any[india_any['primary_num'] > 0]))
print(india_any[india_any['primary_num'] > 0][['reporterISO','reporterDesc','flowCode','primaryValue','primary_num']].head(10).to_string(index=False))



