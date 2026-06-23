{{ config(materialized='view') }}

select
    Video_ID,
    Video_Title,
    Upload_Date,
    Duration,
    Video_Type,
    Video_Views,
    Likes_Count,
    Comments_Count,
from {{ source('youtube', 'yt_api') }}
