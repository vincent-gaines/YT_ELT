select *
from {{ ref('stg_yt_api') }}
where Likes_Count > Video_Views
