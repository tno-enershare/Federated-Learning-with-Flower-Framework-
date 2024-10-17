# Enershare App store integration

This describes how the integration with the app store is proceeding. The store is located at URL: https://store.haslab-dataspace.pt/gui/.

## Status

First publication of the service is online. Some errors prevent the full details to be entered however.

## Message from App store manager

Dear WP6 partners,

We’re ready to proceed with the integration with the App Store, available here: https://store.haslab-dataspace.pt/gui/
The overall documentation is available here: https://store.haslab-dataspace.pt/gui/docs/html/index.html

Integration should comprehend two mains steps:

1. Creating one account and fill up the data space identifiers.
1.1. follow these steps https://store.haslab-dataspace.pt/gui/docs/html/register-user.html
1.2. update the IDS identifier information https://store.haslab-dataspace.pt/gui/docs/html/register-user.html#update-ids-identity-information 
2. Create as many app records as necessary (rule of thumb  one app per service), include their details and create and push app components.
2.1. create the record for one app -> follow these instructions https://store.haslab-dataspace.pt/gui/docs/html/app-lifecycle.html#create-app
2.2. edit its details to complete further information like the readme (advisable). -> https://store.haslab-dataspace.pt/gui/docs/html/app-lifecycle.html#set-edit-app-generic-details
2.3 create app version  https://store.haslab-dataspace.pt/gui/docs/html/app-lifecycle.html#push-new-app-version
2.4 add app components and push contents: component images and docker compose / openapi spec / connector configuration.

For the docker steps you’ll need to collect your client secret and use it as password. Check this link for further details: https://store.haslab-dataspace.pt/gui/docs/html/FAQ.html#get-my-login-secret-from-the-registry

We shall then discuss about the service UIs. If your service / app has a service public UI that can be displayed, come back to me with the URL so that we can embed it within the App Store.

In case of any doubt let us know. Your feedback is important.
