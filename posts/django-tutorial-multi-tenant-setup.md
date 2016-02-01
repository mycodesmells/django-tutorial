# Django Tutorial - Multi Tenant Setup

Recently in a project I'm invoved in, we faced a situation in which we wanted to split the application among several clients in a way, that the data is accessed separately for each of them. On top of that, we wanted to give each client a separate access to the application. Now we could have created appropriate endpoints, or make the user send the client information with each and every request... Fortunately there is a better way - multi-tenant environment. This post allows you to replicate this setup in your own project, step by step.

The most important aspect of multi-tenancy is separating data and its access. The first thing that a user notices when entering such environment, is a specific subdomain via which the app is accessed, such as `client1.app.com`, `client2.app.com` etc. This seems to be a large piece of work, but in fact it is pretty easy to do, especially in Django. 

TODO
- intro
- what is multi-tenancy? why consider it?
- best package solution
- quick setup
- main differences
- etc hosts & allowed hosts
- result