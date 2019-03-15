from enum import Enum


class IntentType(Enum):
    LIST_EC2 = '4eea1776-e8e5-41b5-af37-ae8e46c23e03'
    GET_LOG = 'ad70323d-b173-441f-8d0d-4f10c7fc3e79'
    S3_URL = '35d665c4-9ff9-4686-b7d1-2bc6652dfe83'
    TG_HEALTH = 'ece92beb-df3d-48ee-aefe-2d4f094eba6c'
    TICKET_CREATE = '045bc3cc-5626-4946-9ec0-d8fd2451a784'
    LAUNCH_INSTANCE = '209cbbc6-5998-4339-a3e6-384ef9eef108'

