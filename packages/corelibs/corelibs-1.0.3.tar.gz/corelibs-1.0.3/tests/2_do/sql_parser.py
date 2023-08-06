import sqlparse

query = """
    select sum(mt.data) as sum_data, mt.data_agg
    from (select * from my_table) as mt
    left join my_table_2 as mt2
        on mt.join_id = mt2.join_id
        and mt.join_sub_id = mt2.join_sub_id
    where (mt.id = 20 and mt.time_stamp > "28/11/2013")
    group by mt.data_agg
    having (sum_data > 2 and mt.toto >= 3)
"""
# print(sqlparse.format(query, reindent=True, keyword_case='upper'))

parsed = sqlparse.parse(query)[0]
for _ in parsed:
    if len(str(_)) > 1:
        print(_)
