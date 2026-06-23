select
    Video_ID,
    Video_Title,
    Channel_ID,
    Likes_Count,
    Comments_Count,
    Video_Views,
    Published_At,
    Ingested_At,
    (Likes_Count / nullif(Video_Views, 0)) as like_rate,
    (Comments_Count / nullif(Video_Views, 0)) as comment_rate
from {{ ref('int_yt_api_cleaned') }}
