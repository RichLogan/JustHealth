===========
Development
===========

The JustHealth application was developed using an iterative approach with a strong focus on being as fast and lightweight as possible.

One of the ways we achieved this was through the use of various tools, below is an outline of general development process and how these tools were used in order to improve the way we worked.

---------------------------
General Development Process
---------------------------

Below is outlined the "ideal" process that we aimed to follow for every prece of functionality. We didn't manage to follow this 100% for every little piece of work, but for the most part it worked well. 

1. Identify a piece of functionality to work on
#. Write a card on Trello to document this feature, who is assigned, when it is due and what needs to be done
#. Create a git branch from either master, or an existing parent branch for a wider piece of functionality
#. Write general test cases for this test. Here we would select the inputs and outputs we would expect from a piece of functionality
#. A developer, or pair, would work on this feature, committing work to the git repository
#. Once completed a pull request would be created
#. All tests would be run and the team would review the request
#. On completion of all tests, the pull request would be merged to the parent branch

Our goal with this development process is to ensure that anything on the master branch is deployable at any time. Through the running of tests and review on any pull request, we could attempt to ensure that master was kept clean of any bugs or issues. If an issue was found, it would be logged on the GitHub issues page.

------------------
Development Tools
------------------

------------------
Testing
------------------

We strived to use Test-Driven Development as best we could throughout the entirety of the project. This involves creating tests before any code is written showing the general expected inputs and outputs. The functionality should then be written so that it passes the test. One of the downsides of this approach is that it relies on how well the test covers all eventualities. This did result in tests being rewritten and rerun throughout the entire development time when needed. 

We had numerous types of tests:

1. Automated API tests. 