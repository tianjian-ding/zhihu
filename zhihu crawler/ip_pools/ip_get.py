page = 0
question_id = 1
url = f"""
    https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2\
    Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2\
    Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2\
    Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2\
    Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2C\
    question%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2C\
    is_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2C\
    badge%5B%2A%5D.topics&limit=5&offset={page}&platform=desktop&sort_by=default
"""
print(url)