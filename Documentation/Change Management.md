# Change Management

We have elected to use the source code management software Git in order to control changes, additions and deletions to both our application code and documentation. This will allow all members of the team to add changes without having to worry about conflicts or what the other developers are doing. 

Our code will be hosted on the GitHub website in order to provide an easy and visual way of looking at the state of the repository and the log of all changes. GitHub also provides issue tracking facilities that we will make use of. 

## Development Strategy

Using git, we can develop each of our requirements/features as seperate branches of development, ensuring the master branch is not adversly affected by any of those changes. Once that a feature has been completed and has passed all appropriate tests it can be merged back into the master branch, re-running the tests and certififying that feature as complete. The idea is that everything in Master is always deployable at any time.