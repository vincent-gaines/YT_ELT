select *
from {{ ref('stg_yt_api') }}
where Comments_Count > Video_Views
