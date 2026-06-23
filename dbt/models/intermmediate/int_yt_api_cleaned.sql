select
    *,
    case when Likes_Count is null then 0 else Likes_Count end as Likes_Count_Fill,
    case when Comments_Count is null then 0 else Comments_Count end as Comments_Count_Fill
from {{ ref('core_yt_api') }}

