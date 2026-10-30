# Contributing to this project

First of all, thank you for wanting to contribute.

## How to submit bug reports or feature requests
Bug reports or feature requests can be submitted by opening an issue on
<https://github.com/INCATools/odkcore/issues> or
<https://github.com/INCATools/ontology-development-kit/issues> (but
please favour the former, as the latter should now be reserved for
issues with the Docker images). They may also be sent by e-mail to
<devel@incenp.org>. When using e-mail, please prefix the subject with
`[odk ]`.

## How to submit contributions
Please discuss the change you wish to make first, either through an
issue or by e-mail (see above), before submitting anything.

Contributions can only be submitted by opening a pull request on
<https://github.com/INCATools/odkcore/pulls>. Any contribution sent by e-mail
is likely to be ignored, unless it is a very trivial patch.

Please check your contribution meets the following requirements:

* Python code should pass:
    * the code quality check (`ruff check`);
    * the code formatting check (`ruff format --check`);
    * the static typing check (`mypy`);
    * the spell check (`codespell`);
    * and the Python test suite (`pytest tests`).
* Your patches or commits (when submitting pull requests) should each be
  adequately described by a [meaningful commit
  message](https://incenp.org/dvlpt/docs/vcs-good-practices/index.html#sect.commit-messages).

You _may_ additionally ensure that the seed tests also pass (`cd tests && sh
test-configs.sh`), but this is optional – those tests can take quite a while to
run, so you are _not_ required to run them locally prior to submitting your
contribution as they will be run on the pull request anyway.

## About “generative AI”
Contributions of any kind (code, documentation, tests…) that have been
fully or partially made by genAI tools are discouraged and will be taken
as an admission from you that you are perfectly fine with the
environmental, social, economical, and political external costs
associated with such tools.

Bug reports or feature requests openly or obviously written by genAI
tools are equally discouraged and may be ignored.
