# Profile
- [X] Every user must have his Profile, with having ability of updating contents,
- [X] Watching his friends
- [X] Watching his posts
- [X] Finding of profiles
- [X] Recommendation of profiles base on location, mutual friends 
- [X] Notification of receiving friend Request
- [X] slogan, bio, Name, location and profile picture should be there.
- [X] Show all videos as grid.
- [X] simple search engine, with search by name, location, and tags.


# API Documentations

## Profile Detail View API
 It is designed to retrieve information about a specific user's profile, including statistics and related content such as videos and advertisements.

### Endpoint
- **URL:** `/profiles/<str:pk>/` like abuubaida01
- **HTTP Method:** GET
- **View Class:** `ProfileDetailViewAPI`
- **Name:** `profile-detail-view`

### Permissions
- Public access is allowed (no authentication required).

### Request
- The user profile is determined by the `pk` (primary key) parameter in the URL.
- GET /profiles/abuubaida01/

### Response (HTTP Status 200 - OK)
  Context Object: The response is a JSON object containing information about the specified user's profile, along with other related content that user has created.

  Fields:

  profiles (Object): Contains information about the user's profile serialized using ProfileSerializer.

  pvc_videos (Array, optional): An array of PVC videos associated with the user if available.

  org_videos (Array, optional): An array of org videos associated with the user if available.

  zp (Array, optional): An array of FAM content created by the user if available.

  all_ads (Array, optional): An array of Savads created by the user if available.

  run_pvc (Boolean, optional): Set to true if PVC videos are present.

  run_org (Boolean, optional): Set to true if Org videos are present.

  run_fam (Boolean, optional): Set to true if FAM content is present.

  run_ads (Boolean, optional): Set to true if Savads advertisements are present.

  pvc_count (Integer): The count of PVC videos associated with the user.

  fam_count (Integer): The count of FAM content created by the user.

  org_count (Integer): The count of Org content associated with the user.

  ads_count (Integer): The count of verified and activated Savads advertisements created by the user.

### Example 
```json
{
    "profiles": {
        "id": 1,
        "picture": "/media/media/picture/45-454759_1920x1200-data-id-344972-data-src-walls-full.jpg",
        "intro": "I am software",
        "slogan": "HI jani",
        "profession": "",
        "cur_add": "Karachi",
        "phone_number": null,
        "bank_details": "",
        "fam_post_no": 19,
        "org_post_no": 13,
        "kind": "",
        "reported": false,
        "updated": "2023-10-28T15:45:15.578980+05:00",
        "created": "2023-07-16T17:51:32.182490+05:00",
        "promote": true,
        "restriction_hits": 0,
        "restricted": false,
        "admin_message": "",
        "email_notif": false,
        "cat": "General",
        "user": 1,
        "following": [
            6,
            1
        ]
    },
    "pvc_videos": [
        [
            {
                "id": 51,
                "creator_id": 1,
                "title": "Checking through APIs",
                "description": "Created through API",
                "thumbnail": "",
                "video_link": null,
                "liked": 0,
                "disliked": 0,
                "created": "2023-10-28T07:22:32.944183Z",
                "updated": "2023-10-28T07:22:32.944183Z",
                "reported": false,
                "video": "",
                "gender": "Both",
                "age": "5",
                "keywords": "",
                "restricted": false,
                "anon_views": 0,
                "all_views": 0,
                "ips": "",
                "admin_message": "",
                "slug": "78u2zxnvsdgens1poxlh31dsfkxsdf32v"
            },
            .... other similar objects
        ]
    ],
    "run_pvc": true
}
```




## PVC Videos API

The `PVCVideosAPI` is an API view that allows authenticated users to retrieve a list of PVC (Personal Video Channel) videos created by a specific user profile. This API view provides a way for users to access videos created by the target user, with filtering options based on the user's gender and access privileges.

### Endpoint

- **URL:** `profiles/<str:pk>/pvc` #pk: username
- **HTTP Method:** GET
- **View Class:** `PVCVideosAPI`
- **Name:** `pvc`

### Permissions

- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated to access the list of PVC videos.

### Request
- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to retrieve the list of PVC videos.

### Response (HTTP Status 200 - OK)
```json
[ 
  {
        "id": 36,
        "title": "This is me",
        "description": "",
        "thumbnail": "/media/media/pvc/Thumbnails/45-454759_1920x1200-data-id-344972-data-src-walls-full_KIrSA8f.jpg",
        "video_link": "",
        "liked": 0,
        "disliked": 0,
        "created": "2023-07-25T10:46:26.721070+05:00",
        "updated": "2023-10-05T09:15:24.681376+05:00",
        "reported": false,
        "video": "/media/media/pvc/Videos/3_oyrIXTn.mp4",
        "gender": "Male",
        "age": "5",
        "keywords": "",
        "restricted": false,
        "anon_views": 1,
        "all_views": 3,
        "ips": "127.0.0.1",
        "admin_message": "",
        "slug": "lnv6zlgwvrtqyxgxsuzdatsld-creator-sefarz01kds823vx14",
        "creator": 1,
        "saved": [],
        "uninterested": [],
        "auth_views": [
            8,
            1
        ]
    }
]
```


## Savads List API
  The `SavadsListAPI` is an API view that allows users, whether authenticated or unauthenticated, to retrieve a list of Savads (Advertisements) associated with a specific user or organization profile. This API view provides a way for users to access information about Savads that are both activated and verified and associated with the target user or organization profile.

### Endpoint

- **URL:** `profiles/abuubaida01/ads`
- **HTTP Method:** GET
- **View Class:** `SavadsListAPI`
- **Name:** `ads`

### Permissions
- **Authentication:** This API view is accessible to both authenticated and unauthenticated users, allowing them to retrieve information about activated and verified Savads associated with the specified user or organization profile.

### Request
- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to retrieve the list of Savads.

### Response (HTTP Status 200 - OK)
```json
[
    {
        "id": 25,
        "title": null,
        "description": "hi this is an product",
        "image": null,
        "video": null,
        "deposit_slip": null,
        "product_script": "<script></script>",
        "url": "",
        "phone_number": "",
        "duration": 100,
        "expired": false,
        "activated": true,
        "verified": true,
        "rejected": false,
        "activation_time": "2023-09-24T20:02:10.974908+05:00",
        "keywords": "",
        "high_ava": true,
        "gender": "Males",
        "age": "",
        "created": "2023-09-24T17:33:53.103086+05:00",
        "updated": "2023-10-28T15:57:05.864715+05:00",
        "reported": false,
        "category": "Education",
        "cost": 12500,
        "plan": "everywhere",
        "ano_clicked": 1,
        "anony_ips": "127.0.0.1",
        "admin_message": "",
        "slug": "kaablohyrtqalyxfgbie-advertiser-abuubaida01",
        "creator": 1,
        "clicked": [
            1
        ],
    }
    // ... Other similar Savads objects
]
```


## FAM (Family & Friends) List API

The `FAMListAPI` is an API view that allows users to retrieve a list of family and friends (FAM) associated with a specific user profile. This API view provides a way for users to access information about the FAM members linked to the target user.

### Endpoint
- **URL:** `profiles/abuubaida01/fam`
- **HTTP Method:** GET
- **View Class:** `FAMListAPI`
- **Name:** `fam`

### Permissions
- **Authentication:** This API view is accessible to both authenticated and unauthenticated users, allowing them to retrieve information about the FAM members of a specific user profile.

### Request
- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to retrieve the list of FAM members.

### Response (HTTP Status 200 - OK)
```json
[
    {
        "id": 27,
        "post_number": 19,
        "slug": "788j83ddlrwxoiafxdvgnbjssnprhe",
        "seeker": "",
        "seeker_vid": null,
        "house_vid": null,
        "satisfied_vid": null,
        "phone_number": "",
        "address": "",
        "bank_details": "",
        "needed_money": 0,
        "satisfied": false,
        "content": null,
        "doc1": null,
        "doc2": null,
        "doc3": null,
        "doc4": null,
        "upvote": 0,
        "downvote": 0,
        "created": "2023-10-28T15:27:14.290846+05:00",
        "blur_face": false,
        "kind": "",
        "reported": false,
        "updated": "2023-10-28T15:27:14.298346+05:00",
        "without_house": true,
        "verified": 100,
        "paid": 0,
        "admin_message": null,
        "creator": 1,
        "saved": [],
        "donor": []
    },
    // ... Other similar FAM member objects
]
```


## Organization Videos List API

The `OrgVideosListAPI` is an API view that allows users, whether authenticated or unauthenticated, to retrieve a list of videos associated with a specific organization or user profile. This API view provides a way for users to access information about videos created or associated with the target organization or user.

### Endpoint

- **URL:** `profiles/abuubaida01/org`
- **HTTP Method:** GET
- **View Class:** `OrgVideosListAPI`
- **Name:** `org`

### Permissions
- **Authentication:** This API view is accessible to both authenticated and unauthenticated users, allowing them to retrieve information about videos associated with the specified organization or user profile.

### Request
- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to retrieve the list of videos.

### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 27,
        "creator": "Abdul Hafeez",
        "phone_number": "+92 331 2371338",
        "address": "Karachi",
        "bank_details": null,
        "creator_vid": null,
        "org_vid": null,
        "satisfied_vid": null,
        "verified": true,
        "paid": 0,
        "needed_money": 0,
        "satisfied": false,
        "upvote": 0,
        "downvote": 0,
        "created": "2023-10-28T15:11:46.126985+05:00",
        "post_number": 13,
        "docs": null,
        "reported": false,
        "updated": "2023-10-28T15:11:46.126985+05:00",
        "message": null,
        "slug": "dmm7rjnsl5blzkxvr1fnnbnftrsfq9",
        "admin_message": "",
        "org_name": 1,
        "donor": [],
        "saved": []
    },
    // ... Other similar video objects
]
```



## Profile List API

The `ProfileListAPI` is an API view that provides a list of user profiles. It serves two distinct purposes based on the authentication status of the requesting user. For authenticated users, it provides a list of recommended profiles. For unauthenticated users, it offers a list of general user profiles, filtered by gender and category.

### Endpoint
- **URL:** `/profiles/allp/`
- **HTTP Method:** GET
- **View Class:** `ProfileListAPI`
- **Name:** `all-profiles`

### Permissions
- Users must be authenticated in to order to access recommended profiles.
- For unauthenticated users, Random Male Profiles are only Displayed

### Request

- The API view does not require any request parameters.
- The behavior is determined by the authentication status of the user making the request.

### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 43,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "",
        "slogan": "",
        "profession": "",
        "cur_add": "",
        "phone_number": null,
        "bank_details": "",
        "fam_post_no": 0,
        "org_post_no": 0,
        "kind": "",
        "reported": false,
        "updated": "2023-10-10T00:18:20.004934+05:00",
        "created": "2023-10-10T00:18:20.004934+05:00",
        "promote": false,
        "restriction_hits": 0,
        "restricted": false,
        "admin_message": "",
        "email_notif": false,
        "cat": "General",
        "user": 43,
        "following": []
    },
    ..... Other Similar profiles objects  
]
```


## Organization List API

The `OrgListAPIView` is an API view that serves as a source of user profiles, specifically focusing on organization profiles. Similar to the `ProfileListAPI`, it offers two different functionalities based on the authentication status of the requesting user: recommended organization profiles for authenticated users and a list of general organization profiles for unauthenticated users.

### Endpoint

- **URL:** `/profiles/organizations`
- **HTTP Method:** GET
- **View Class:** `OrgListAPIView`
- **Name:** `all-organizations`

### Permissions

- **Authentication Required:** For authenticated users, this API view requires user authentication to access recommended organization profiles.
- **Unauthenticated Access:** Unauthenticated users have access to view a list of general organization profiles.

### Request

- This API view does not require any request parameters.
- The behavior depends on the authentication status of the user making the request.

### Response (HTTP Status 200 - OK)

The response is a JSON array containing organization profile objects. Each organization profile object has the following fields:

```json
[
    {
        "id": 15,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "",
        "slogan": "",
        "profession": "",
        "cur_add": "",
        "phone_number": null,
        "bank_details": "",
        "fam_post_no": 0,
        "org_post_no": 0,
        "kind": "",
        "reported": false,
        "updated": "2023-08-18T17:24:37.467664+05:00",
        "created": "2023-08-18T11:21:19.049119+05:00",
        "promote": false,
        "restriction_hits": 0,
        "restricted": false,
        "admin_message": "",
        "email_notif": true,
        "cat": "Organization",
        "user": 15,
        "following": []
    },
    // ... Other similar organization profile objects
]
```



## Channel List API

The `ChannelListAPIView` is an API view that provides a list of user profiles with a focus on channel profiles. It offers two different functionalities depending on the authentication status of the requesting user: recommended channel profiles for authenticated users and a list of general channel profiles for unauthenticated users.

### Endpoint

- **URL:** `/profiles/Channels`
- **HTTP Method:** GET
- **View Class:** `ChannelListAPIView`
- **Name:** `all-cha`

### Permissions

- **Authentication Required:** For authenticated users, this API view requires user authentication to access recommended channel profiles.
- **Unauthenticated Access:** Unauthenticated users have access to view a list of general channel profiles.

### Request

- This API view does not require any request parameters.
- The behavior depends on the authentication status of the user making the request.

### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 43,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "",
        "slogan": "",
        "profession": "",
        "cur_add": "",
        "phone_number": null,
        "bank_details": "",
        "fam_post_no": 0,
        "org_post_no": 0,
        "kind": "",
        "reported": false,
        "updated": "2023-10-10T00:18:20.004934+05:00",
        "created": "2023-10-10T00:18:20.004934+05:00",
        "promote": false,
        "restriction_hits": 0,
        "restricted": false,
        "admin_message": "",
        "email_notif": false,
        "cat": "Channel",
        "user": 43,
        "following": []
    },
    // ... Other similar channel profile objects
]
```



## Masjid & Madrasa List API

The `MListAPIView` is an API view that provides a list of user profiles, with a specific focus on Masjid and Madrasa profiles. Similar to the previous API views, it offers two different functionalities based on the authentication status of the requesting user: recommended Masjid and Madrasa profiles for authenticated users and a list of general Masjid and Madrasa profiles for unauthenticated users.

### Endpoint

- **URL:** `/profiles/M&M`
- **HTTP Method:** GET
- **View Class:** `MListAPIView`
- **Name:** `all-mm`

### Permissions

- **Authentication Required:** For authenticated users, this API view requires user authentication to access recommended Masjid and Madrasa profiles.
- **Unauthenticated Access:** Unauthenticated users have access to view a list of general Masjid and Madrasa profiles.

### Request

- This API view does not require any request parameters.
- The behavior depends on the authentication status of the user making the request.

### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 43,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "",
        "slogan": "",
        "profession": "",
        "cur_add": "",
        "phone_number": null,
        "bank_details": "",
        "fam_post_no": 0,
        "org_post_no": 0,
        "kind": "",
        "reported": false,
        "updated": "2023-10-10T00:18:20.004934+05:00",
        "created": "2023-10-10T00:18:20.004934+05:00",
        "promote": false,
        "restriction_hits": 0,
        "restricted": false,
        "admin_message": "",
        "email_notif": false,
        "cat": "Masjid & Madrasa",
        "user": 43,
        "following": []
    },
    ..... Other Similar profiles objects  
]
```


## Brand List API

The `BrandListAPIView` is an API view that provides a list of user profiles, with a specific focus on brand profiles. Similar to the previous API views, it offers two different functionalities based on the authentication status of the requesting user: recommended brand profiles for authenticated users and a list of general brand profiles for unauthenticated users.

### Endpoint

- **URL:** `/profiles/Brands`
- **HTTP Method:** GET
- **View Class:** `BrandListAPIView`
- **Name:** `all-b`

### Permissions

- **Authentication Required:** For authenticated users, this API view requires user authentication to access recommended brand profiles.
- **Unauthenticated Access:** Unauthenticated users have access to view a list of general brand profiles.

### Request

- This API view does not require any request parameters.
- The behavior depends on the authentication status of the user making the request.

### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 43,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "",
        "slogan": "",
        "profession": "",
        "cur_add": "",
        "phone_number": null,
        "bank_details": "",
        "fam_post_no": 0,
        "org_post_no": 0,
        "kind": "",
        "reported": false,
        "updated": "2023-10-10T00:18:20.004934+05:00",
        "created": "2023-10-10T00:18:20.004934+05:00",
        "promote": false,
        "restriction_hits": 0,
        "restricted": false,
        "admin_message": "",
        "email_notif": false,
        "cat": "Brand",
        "user": 43,
        "following": []
    },
    // ... Other similar brand profile objects
]
```

documentation for the `NearMeListAPI` class in your Django application:

## Near Me List API
    Here if user is authenticated and he/she has provided address, then list of nearby profiles will be return to that user.

### Endpoint
- **URL:** `/profiles/<str:pk>/nearme`
- **HTTP Method:** GET
- **View Class:** `NearMeListAPI`
- **Name:** `near_me`

### Permissions

- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated.

### Request

- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to find nearby profiles.

### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 51,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "Exploring the world through photography.",
        "slogan": "Capturing moments, creating memories.",
        "profession": "Photographer",
        "cur_add": "123 Photography Street, Shutter Town",
        "phone_number": "555-123-4567",
        "bank_details": "PhotoBank, Account #9876",
        "reported": false,
        "updated": "2023-10-12T11:18:30.004934+05:00",
        "created": "2023-08-20T09:30:45.002718+05:00",
        "email_notif": true,
        "cat": "General",
        "user": 51,
        "following": [3, 7, 9]
    },
    // ... Other similar profile objects located nearby
]
```


## Profile Update API

The `ProfileUpdateAPI` is an API view that allows authenticated users to retrieve and update their user profile information. Users can make partial or complete updates to their profile data, including fields like introduction, slogan, profession, address, phone number, and more.

### Endpoint

- **URL:** `profiles/update`
- **HTTP Method:** GET (Retrieve Profile), PUT/PATCH (Update Profile)
- **View Class:** `ProfileUpdateAPI`
- **Name:** `profile_update`

### Permissions

- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated to access their profile and update it.

### Request (Update Profile)

- **HTTP Method:** PUT (Full Update) or PATCH (Partial Update)
- Users can send a PUT or PATCH request to update their profile data. The request should include the fields to be updated in the request data.

- **HTTP Method:** GET
- The user can send a GET request to retrieve their own profile information.


### Response (Update Profile) (HTTP Status 200 - OK)

```json
{
    "id": 37,
    "picture": "http://localhost:8000/media/media/picture.jpg",
    "intro": "A nature enthusiast sharing the beauty of the outdoors.",
    "slogan": "Explore, appreciate, protect.",
    "profession": "Environmentalist",
    "cur_add": "789 Nature Lane, Scenic Valley",
    "phone_number": "555-789-1234",
    "bank_details": "EcoBank, Account #54321",
    "reported": false,
    "updated": "2023-11-05T14:25:30.002118+05:00",
    "created": "2023-08-25T13:30:15.002718+05:00",
    "email_notif": true,
    "cat": "General",
    "user": 37,
    "following": [5, 8, 12]
}
```


## Follow/Unfollow API

The `FollowUnfollowAPI` is an API view that allows authenticated users to follow or unfollow other users. This API view enables users to establish or remove a following relationship with another user, and it provides options for notifications and email notifications.

### Endpoint

- **URL:** `profiles/<str:pk>/follow`
- **HTTP Method:** POST
- **View Class:** `FollowUnfollowAPI`
- **Name:** `follow-unfollow-profile`

### Permissions

- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated to follow or unfollow other users.

### Request (Follow or Unfollow)

- **Path Parameter:** `{pk}` - The unique identifier (username) of the user you want to follow or unfollow.

### Response (HTTP Status 200 - OK)  (Follow) and (Unfollow)
- `status` (String): Indicates the status of the follow/unfollow action. It can be 'Follow' if the user has been followed or 'UnFollow' if the user has been unfollowed.

```json
{
    "status": "Follow"
}
       or
{
    "status": "UnFollow"
}
```



## Remove Follower API

The `remove_followerAPI` is an API view that allows authenticated users to remove a follower from their profile. This API view enables users to manage their list of followers by removing specific users from the list.

### Endpoint

- **URL:** `profiles/<str:pk>/removefollower`
- **HTTP Method:** POST
- **View Class:** `remove_followerAPI`
- **Name:** `remove-follower`

### Permissions
- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated to remove a follower from their profile.

### Request (Remove Follower)
- **Path Parameter:** `{pk}` - The unique identifier (username) of the follower you want to remove from your profile.

### Response (HTTP Status 200 - OK)
- `message` (String): A message indicating that the follower has been removed.

```json
{
    "message": "Removed Follower"
}
```



## Follower List API
The `FollowerListAPI` is an API view that allows authenticated users to retrieve a list of profiles that are following a current user(him/her). 

### Endpoint

- **URL:** `/profiles/<str:pk>/followers`
- **HTTP Method:** GET
- **View Class:** `FollowerListAPI`
- **Name:** `followers`

### Permissions

- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated to access the list of followers for a specific user.

### Request

- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to retrieve the list of followers.

### Response (HTTP Status 200 - OK)
```json
[
    {
        "id": 29,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "A photography enthusiast capturing moments.",
        "slogan": "Exploring the world one click at a time.",
        "profession": "Photographer",
        "cur_add": "456 Shutter Street, Focusville",
        "phone_number": "555-456-7890",
        "bank_details": "PhotoBank, Account #87654",
        "reported": false,
        "updated": "2023-09-28T08:45:15.002918+05:00",
        "created": "2023-08-10T12:20:30.003126+05:00",
        "email_notif": true,
        "cat": "General",
        "user": 29,
        "following": [4, 8, 12]
    },
    // ... Other similar follower profile objects
]
```





## Following List API
The `FollowingListAPI` is an API view that allows authenticated users to retrieve a list of profiles that they are following. 

### Endpoint
- **URL:** `/profiles/<str:pk>/following`
- **HTTP Method:** GET
- **View Class:** `FollowingListAPI`
- **Name:** `following`


### Permissions
- **Authentication Required:** This API view requires user authentication, and the requesting user must be authenticated to access their list of followed profiles.


### Request
- **Path Parameter:** `{pk}` - The unique identifier (username) of the user for whom you want to retrieve the list of profiles they are following.


### Response (HTTP Status 200 - OK)

```json
[
    {
        "id": 18,
        "picture": "http://localhost:8000/media/media/picture.jpg",
        "intro": "Passionate about cooking and sharing recipes.",
        "slogan": "Cooking is an art, and I'm the artist.",
        "profession": "Chef",
        "cur_add": "123 Culinary Lane, Flavorville",
        "phone_number": "555-123-9876",
        "bank_details": "TasteBank, Account #87621",
        "reported": false,
        "updated": "2023-10-05T15:30:10.002518+05:00",
        "created": "2023-08-15T10:50:25.004712+05:00",
        "email_notif": true,
        "cat": "General",
        "user": 18,
        "following": [6, 12, 15]
    },
    // ... Other similar followed profile objects
]
```




## User Search API

The `UserVuzerAPI` is an API view that allows both authenticated and unauthenticated users to search for user profiles based on specific search criteria. Users can search for profiles by a query term and filter the results by category.

### Endpoint

- **URL:** `profiles/search?query=k&category=General`
- **HTTP Method:** GET
- **View Class:** `UserVuzerAPI`
- **Name:** `search-user`

### Permissions
- **Authentication:** This API view allows both authenticated and unauthenticated users to search for user profiles.

### Request
- **Query Parameters:**
  - `query` (String, required): The search query term to find user profiles.
  - `category` (String, required): The category by which to filter the search results.
  - http://127.0.0.1:8000/profiles/search?query=karachi&category=General 


### Response (HTTP Status 200 - OK)
```json
{
    "search_list": [
        {
            "id": 43,
            "picture": "http://127.0.0.1:8000/media/media/picture.jpg",
            "intro": "",
            "slogan": "",
            "profession": "",
            "cur_add": "",
            "phone_number": null,
            "bank_details": "",
            "fam_post_no": 0,
            "org_post_no": 0,
            "kind": "",
            "reported": false,
            "updated": "2023-10-10T00:18:20.004934+05:00",
            "created": "2023-10-10T00:18:20.004934+05:00",
            "promote": false,
            "restriction_hits": 0,
            "restricted": false,
            "admin_message": "",
            "email_notif": false,
            "cat": "General",
            "user": 43,
            "following": []
        },
        // ... Other similar user profile objects
    ]
}
```