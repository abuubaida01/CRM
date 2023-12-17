## SUPPORT
[x] Report user, Zakat, PVC, Sefarz issue
[x] Suggestion to savior


# API Documentations


# Suggestion to Savior API
The `Sugg2SaviorAPIView` allows authenticated users to submit suggestions to the Sefarz platform. Users can provide feedback, ideas, or recommendations, which are then forwarded to the platform administrators for consideration and potential implementation.

## Endpoint
- **URL:** `/support/sugg2savior/`
- **HTTP Method:** POST
- **View Class:** `Sugg2SaviorAPIView`
- **Name:** `Sugg2SaviorFunc`

## Permissions
- This API view is accessible only to authenticated users.

## Request Parameters
- `suggestion` (POST parameter): The user's suggestion, feedback, or idea to be submitted to the platform.

## Response (HTTP Status 201 - Created)
```json
{
    "message": "Your suggestion has been sent to the Sefarz team. We will check it out. Thanks for your suggestion!"
}
      or
{
    "message": "You have sent nothing :)"
}
```




# Report PVC Function API
The `ReportpvcFuncAPI` is an API view that allows authenticated users to report a PVC video on the Sefarz platform. Users can report videos that violate community guidelines or contain inappropriate content. This function enables users to contribute to the platform's content moderation and safety.

## Endpoint

- **URL:** `/support/Reportpvc/`
- **HTTP Method:** POST
- **View Class:** `ReportpvcFuncAPI`
- **Name:** `ReportpvcFunc`

## Permissions
- Only authenticated users are allowed to access this API view.

## Request Parameters

- `slug` (POST parameter): The unique identifier (slug) of the PVC video that the user wants to report.
- `body` (POST parameter): The description or details of the problem or violation found in the reported video.

## Response
```json
{
    "message": "You have reported [creator's name] for [problem]. We are sorry for this inconvenience, and we will check it out."
}
```
### Already Reported Video
**Example Error Response:**
```json
{
    "message": "You have already reported this video"
}
 or
{
    "message": "You have reported nothing :)"
}
```


# Report Savads API
The `ReportSavadsAPI` is an API view that allows authenticated users to report a Savads advertisement on the Sefarz platform. Users can report ads that violate community guidelines or contain inappropriate content. This function enables users to contribute to the platform's content moderation and safety.

## Endpoint
- **URL:** `/savads/ReportSavads/`
- **HTTP Method:** POST
- **View Class:** `ReportSavadsAPI`
- **Name:** `ReportSavads`

## Permissions
- Only authenticated users are allowed to access this API view.

## Request Parameters

- `slug` (POST parameter): The unique identifier (slug) of the Savads advertisement that the user wants to report.
- `body` (POST parameter): The description or details of the problem or violation found in the reported advertisement.

## Response
```json
{
    "message": "You have reported [ad creator's name] for [problem]. We are sorry for this inconvenience, and we will check it out."
}
```
### Already Reported Advertisement
```json
{
    "message": "You have already reported this advertisement"
}
    or
{
    "message": "You have reported nothing :)"
}
```

# Report Zakat Post API
The `ReportZakatPostAPI` is an API view that allows authenticated users to report a Zakat post on the Sefarz platform. Users can report Zakat posts that violate community guidelines or contain inappropriate content. This function enables users to contribute to the platform's content moderation and safety.

## Endpoint

- **URL:** `/savads/ReportZakatPost/`
- **HTTP Method:** POST
- **View Class:** `ReportZakatPostAPI`
- **View Class:** `ReportZakatPostFunc`

## Permissions
- Only authenticated users are allowed to access this API view.

## Request Parameters
- `slug` (POST parameter): The unique identifier (slug) of the Zakat post that the user wants to report.
- `body` (POST parameter): The description or details of the problem or violation found in the reported Zakat post.

## Response
```json
{
    "message": "Thank you for your report regarding ([user's full name]) for ([problem]). We apologize for the inconvenience caused and will investigate promptly. The report count will be updated soon."
}
```

### Invalid Report
```json
{
    "paid": false,
    "message": "Something went wrong, please refresh the page and try again :("
}
      or
{
    "message": "You have already reported this Seeker"
}
      or
{
    "message": "You have reported nothing :)"
}
```


# Report User API

The `ReportUserAPI` is an API view that allows authenticated users to report other users on the Sefarz platform. Users can report individuals who violate community guidelines or engage in inappropriate behavior. This function enables users to contribute to the platform's content moderation and community safety.

## Endpoint

- **URL:** `/support/ReportUser/`
- **HTTP Method:** POST
- **View Class:** `ReportUserAPI`
- **Name:** `ReportUserFunc`

## Permissions

- Only authenticated users are allowed to access this API view.

## Request Parameters

- `username` (POST parameter): The username of the user that the reporting user wants to report.
- `problem` (POST parameter): A description or details of the problem or violation associated with the reported user.

## Response

Upon successfully reporting another user, the API responds with a confirmation message.

**Example Response:**
```json
{
    "message": "You have reported ([reported user's full name]) for ([problem]). We are sorry for this inconvenience, we will check it out."
}
```

### Account Restriction

- If the reported user has been reported 10 times or more, their account is marked as "reported" and restricted. In this case, the API will respond with an error message indicating that the reported user's account has been restricted.

```json
{
    "message": "Your account has been restricted."
}
        or
{
    "Message": "You have already reported this user"
}
        or
{
    "Message": "You have reported nothing :)"
}
```



# Report Organization API

The `ReportOrgAPI` is an API view that allows authenticated users to report organizations on the Sefarz platform. Users can report organizations that violate community guidelines or engage in inappropriate behavior. This function enables users to contribute to the platform's content moderation and community safety.

## Endpoint

- **URL:** `support/ReportOrgFunc/`
- **HTTP Method:** POST
- **View Class:** `ReportOrgAPI`
- **Name:** `ReportOrgFunc`

## Permissions

- Only authenticated users are allowed to access this API view.

## Request Parameters

- `slug` (POST parameter): The unique identifier (slug) of the organization that the reporting user wants to report.
- `problem` (POST parameter): A description or details of the problem or violation associated with the reported organization.

## Response

Upon successfully reporting an organization, the API responds with a confirmation message.

**Example Response:**
```json
{
    "message": "Thank you for your report regarding ([reported organization name]) for ([problem]). We apologize for the inconvenience caused and will investigate it as soon as possible. The report count will be updated soon."
}
```

### Account Restriction

- If the reported organization has been reported 10 times or more, their account is marked as "reported" and restricted. In this case, the API will respond with an error message indicating that the organization's account has been restricted.

**Example Error Response:**
```json
{
    "message": "Account has been restricted."
}
```

### Already Reported Organization

- If the reporting user has already reported the same organization, the API will respond with an error message.

**Example Error Response:**
```json
{
    "message": "You have already reported this organization"
}
        or
{
    "message": "You have reported nothing :)"
}
```
