How to contribute
=================

We have just started! Our aim is to make the Khiva library the reference library for time series analysis in the fastest fashion.
To achieve this target we need your help!

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome. If you
want to add one or two interesting feature calculators, implement a new feature selection process or just fix 1-2 typos,
your help is appreciated.

If you want to help, just create a pull request on our github page.


Guidelines
''''''''''
Branching model
++++++++++++++++
Our branching model has one permanent branch, **master**. We aim at using `master` as the main branch, where all
features are merged. In this sense, we also use the master branch to contain the release versions of the Python Khiva library
by means of git tags.

Contribution process
+++++++++++++++++++++
In order to contribute to the code base, we follow the next process:

1. The main branch is `master`, every developer should pull the current status of the branch before stating to develop any new feature.
`git pull`

2. Create a new branch with the following pattern "feature/[name_of_the_feature]"
`git checkout -b feature/example_feature`

3. Develop the new feature on the the new branch. It includes testing and documentation.
`git commit -a -m "Bla, Bla, Bla"`

`git push`

4. Open a Pull Request to merge the feature branch in to `master`. Currently, a pull request has to be reviewed at least by
one person.

5. Finally, delete the feature branch.

6. Move back to `master` branch.
`git checkout master`

7. Pull the latest changes.
`git pull`
