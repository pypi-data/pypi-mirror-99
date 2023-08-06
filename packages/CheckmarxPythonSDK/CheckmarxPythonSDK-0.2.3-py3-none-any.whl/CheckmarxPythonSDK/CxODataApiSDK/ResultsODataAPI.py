from .HttpRequests import get_request


def get_results_for_a_specific_scan_id(scan_id):
    """
    http://localhost/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=0
    http://localhost/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=10

    Args:
        scan_id (int):

    Returns:
        `list` of `dict`

        example:
        [
        {
        'Id': 4, 'ResultId': '1000012-4', 'ScanId': 1000012, 'SimilarityId': 1937265109, 'RawPriority': None,
        'PathId': 4, 'ConfidenceLevel': 95, 'Date': '2020-11-06T16:32:07.603+08:00', 'Severity': 'High', 'StateId': 0,
        'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None, 'QueryId': 589, 'QueryVersionId': 56089346
        }
        ]
    """

    url = "/Cxwebinterface/odata/v1/Scans({ScanId})/Results".format(
        ScanId=scan_id
    )

    return get_request(relative_url=url)


def get_the_query_that_was_run_for_a_particular_unique_scan_result(result_id, scan_id):
    """
    Requested result: selects a particular unique scan result and lists the query (SQL Injection, etc.) that was run

    Query used for retrieving the data:
    http://localhost/Cxwebinterface/odata/v1/Results(Id=18,ScanId=1000001)?$expand=Query($select=Name)

     Args:
        result_id (int):
        scan_id (int):

    Returns:
        str
    """
    url = ("/Cxwebinterface/odata/v1/Results(Id={id},ScanId={ScanId})"
           "?$expand=Query($select=Name)").format(
        id=result_id,
        ScanId=scan_id
    )

    query_list = get_request(relative_url=url)

    if not query_list:
        return None

    return query_list[0].get("Query").get("Name")


def get_results_for_a_specific_scan_id_with_query_language_state(scan_id, filter_false_positive=False):
    """

    might need to read in page mode

    Args:
        scan_id (int):
        filter_false_positive (bool): filter False positive (eg. only choose [Propose] Not Exploitable)

    Returns:
        list of dict

        example:
        [
        {
        'ResultId': 2, 'QueryId': 589, 'QueryName': 'Connection_String_Injection',
        'QueryGroupName': 'Java_High_Risk', 'LanguageName': 'Java', 'StateName': 'Not Exploitable'
        },
        {
        'ResultId': 73, 'QueryId': 591, 'QueryName': 'Reflected_XSS_All_Clients',
        'QueryGroupName': 'Java_High_Risk', 'LanguageName': 'Java', 'StateName': 'To Verify'
        }
        ]
    """
    # have to put ScanId in url, otherwise would have deserialization error
    url = ("/Cxwebinterface/odata/v1/Scans({id})/Results?$select=Id,ScanId,QueryId,SimilarityId"
           "&$expand=Query($select=Name;$expand=QueryGroup($select=Name,"
           "LanguageName)),State($select=Name)").format(
        id=scan_id
    )

    if filter_false_positive:
        url += "&$filter=State/Id eq 1 or State/Id eq 4"

    item_list = get_request(relative_url=url)

    results = [
        {
            "SimilarityId": item.get("SimilarityId"),
            "Language": item.get("Query").get("QueryGroup").get("LanguageName"),
            "QueryGroup": item.get("Query").get("QueryGroup").get("Name"),
            "Query": item.get("Query").get("Name"),
            "QueryId": item.get("QueryId"),
            "ResultId": item.get("Id"),
            "ResultState": item.get("State").get("Name")
        } for item in item_list
    ]

    results = sorted(results, key=lambda re: (re.get("Language"), re.get("QueryGroup"),
                                              re.get("QueryId"), re.get("ResultId"), ))
    return results


def get_results_group_by_query_id_and_add_count_json_format(scan_id, filter_false_positive=False,
                                                            threshold=0):
    """

    Args:
        scan_id (int):
        filter_false_positive (bool):
        threshold (int): minimum value of Count

    Returns:

    """
    re = get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=scan_id, filter_false_positive=filter_false_positive
    )

    results = []

    from itertools import groupby
    # first group by LanguageName
    re = sorted(re, key=lambda result: result.get("Language"))
    for _, language_group in groupby(re, lambda result: result.get("Language")):
        l_list = list(language_group)
        language_name = l_list[0].get("Language")
        query_group_list = []
        results.append(
            {
                "Language": language_name,
                "QueryGroupList": query_group_list
            }
        )

        # second group by QueryGroupName
        l_list = sorted(l_list, key=lambda result: result.get("QueryGroup"))
        for _, query_group_group in groupby(l_list, lambda result: result.get("QueryGroup")):
            l_query_group = list(query_group_group)
            query_group_name = l_query_group[0].get("QueryGroup")
            query_list = []
            query_group_list.append(
                {
                    "QueryGroup": query_group_name,
                    "QueryList": query_list
                }
            )

            # third group by QueryName/QueryId
            l_query_group = sorted(l_query_group, key=lambda r: r.get("QueryId"))
            for _, query_group in groupby(l_query_group, lambda r: r.get("QueryId")):
                l_query_name = list(query_group)
                query_name = l_query_name[0].get("Query")

                count = len(l_query_name)
                # ignore those queries that count smaller than threshold
                if count < threshold:
                    continue

                query_list.append(
                    {
                        "Query": query_name,
                        "Count": count
                    }
                )

    return results
