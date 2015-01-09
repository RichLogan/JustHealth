===========
Development
===========

The JustHealth application was developed using an iterative approach with a strong focus on being as fast and lightweight as possible.

One of the ways we achieved this was through the use of various tools, below is an outline of general development process and how these tools were used in order to improve the way we worked.

--------------
Git and GitHub
--------------

---------------------------
General Development Process
---------------------------

1. Identify a piece of functionality to work on
2. Create a git branch from either master, or an existing parent branch for a wider piece of functionality
3. Write general test cases for this test. Here we would select the inputs and outputs we would expect from a piece of functionality
4. Write a card on Trello to document this feature, who is assigned, when it is due and what needs to be done
5. A developer, or pair, would work on this feature, committing work to the git repository
6. Once completed a pull request would be created
7. All tests would be run and the team would review the request
8. On completion of all tests, the pull request would be merged to the parent branch


Our goal with this development process is to ensure that anything on the master branch is deployable at any time. Through the running of tests and review on any pull request, we could attempt to ensure that master was kept clean of any bugs or issues. If an issue was found, it would be logged on the GitHub issues page.
