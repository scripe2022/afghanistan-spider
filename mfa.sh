for i in {1..9}
do
    curl 'https://www.mfa.gov.cn/irs/front/search' \
    -H 'Accept: application/json, text/javascript, */*; q=0.01' \
    -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/json' \
    -H 'Cookie: HMF_CI=2969709230e5f18f096ce2eab9894c15c05f8b20673bda37cb68c55dea50a8315944a1df1fa97e6a904b5904d1e8827876b33af5021935509ebc656c0263327a44; _trs_uv=lb16qh67_469_hjs' \
    -H 'Origin: https://www.mfa.gov.cn' \
    -H 'Referer: https://www.mfa.gov.cn/irs-c-web/search.shtml?dataTypeId=15&code=17e50b77dab&codes=&configCode=&advancedFilters=%5B%7B%22fieldId%22%253A%22%22%252C%22fieldName%22%253A%22containsAll%22%252C%22searchWord%22%253A%5B%22%E9%98%BF%E5%AF%8C%E6%B1%97%22%5D%7D%252C%7B%22fieldId%22%253A%22%22%252C%22fieldName%22%253A%22containsOne%22%252C%22searchWord%22%253A%5B%5D%7D%252C%7B%22fieldId%22%253A%22%22%252C%22fieldName%22%253A%22none%22%252C%22searchWord%22%253A%5B%5D%7D%5D&isDefaultAdvanced=1&appendixType=&granularity=CUSTOM&orderBy=related&searchBy=all&beginDateTime=2021-08-15&endDateTime=2021-09-15&sign=27551d2a-6933-4e9c-cfd8-1fa50974e463' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' \
    -H 'X-Requested-With: XMLHttpRequest' \
    -H 'sec-ch-ua: "Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Linux"' \
    --data-raw '{"code":"17e50b77dab","configCode":"","codes":"","searchWord":"","historySearchWords":[],"dataTypeId":"15","orderBy":"related","searchBy":"all","appendixType":"","granularity":"CUSTOM","beginDateTime":1629010800000,"endDateTime":1631775599999,"isSearchForced":0,"filters":[],"pageNo":'$i',"pageSize":10,"isDefaultAdvanced":"1","advancedFilters":[{"fieldId":"","fieldName":"containsAll","searchWord":["阿富汗"]},{"fieldId":"","fieldName":"containsOne","searchWord":[]},{"fieldId":"","fieldName":"none","searchWord":[]}],"isAdvancedSearch":1}' \
    --compressed \
    > mfalinks/page$i.json
done