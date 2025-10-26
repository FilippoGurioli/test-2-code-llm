# Audit and Future Work

## Future improvements

The project intentionally provides generic interfaces in specific parts of the codebase in order to allow me to exploit a simplified implementation but also to allow future improvements and extensions. Some of the possible improvements that can be made to the project are:

- **Switch to Docker sandbox environment**: currently the code is executed in a local sandboxed environment using `pytest` and `venv`. A more robust solution would be to use Docker containers to isolate the execution environment and ensure consistency across different runs.
- **Add more LLM models**: currently only a limited number of LLMs are supported. Adding support for more models would allow for a more comprehensive comparison and selection of the best model for specific tasks.
- **Add support for more test suites and languages**: currently only Python and pytest are supported. Adding support for more programming languages and test frameworks would make the tool more versatile and applicable to a wider range of scenarios.

If we go back to requirements we can see that not all the main objectives have been fully achieved. In particular, it was not possible to create a fully automated pipeline that can be used in real-world scenarios. This was mainly due to time constraints. A good improvement thus could be to create a GitHub Action workflow that can be triggered on pull requests to automatically generate code based on tests provided in the PR.

## Audit

Python was chosen as the programming language for this project due to its widely recognized strengths in machine learning libraries. However, the last time I used python was more than a year ago, so first weeks were completely spent in re-familiarizing myself with the language and its ecosystem as well as imposing a solid typing discipline to my code.

I must admit that the prototyping capability of python were really helpful during all the phases of the project. I really think that I've found the sweet spot between a more-or-less strict typing system and the flexibility of a dynamic language.

I really like how the project turned out, I enjoyed a lot the design phase and I think that no major design flaws were made. The modularity of the codebase allowed me to easily extend and modify different parts of the project without affecting the overall structure. Moreover, the modular design also allowed me to struggle for perfection in concepts while providing simplified implementations that let me meet the deadlines (e.g. design a *sandbox environment* as a sterile testing ground while implementing it as not-very-sterile local environment).

### About experiment

The overall experiment could be thought as successful, since it demonstrated the feasibility of using LLMs for automated code generation guided by tests. The insights gained from the analysis can help in selecting the most suitable LLM and test types for specific coding tasks, ultimately improving the efficiency and reliability of code generation processes. The manual testing with more advanced models further confirms the fact that its just a matter of time before LLMs become reliable tools for code generation in real-world scenarios and maybe, that time is even now.
