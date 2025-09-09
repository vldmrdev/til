I noticed that concepts like llms.txt or AGENTS.md have emerged for LLMs-files that duplicate the structure of your website or documentation for a more accurate understanding of information for LLMs. This is a clear idea; it's useful, and I think it can be applied to many cases, such as articles, books, or describing the structure of your project. However, similar files are also created for humans, so why duplicate? At least, we shouldn't have to create such files manually. I think that for such cases, additional LLM markup in HTML or Markdown is needed, which would allow us to annotate text specifically for LLMs within human-readable text, thus avoiding duplication. For example:

```html
<llm-title point="1"> This is a title of section or subsection of you text </llm-title>

<llm-short-description point="1"> This is a short description that’s linked to the title marked "point=1".</llm-short-description>

<llm-description point="1"> This idea can be expanded: additional tags could be added so an LLM can read a page’s source using those tags, or so the creation of the required llm-files could be automated from the tags. The same approach could work for other text types (articles, READMEs, etc.). Text editors will need new features to support this. </llm-description>
```

or

```markdown
#%[1] This is a title of section or subsection of you text. 
##%[1] This is a short description.
###%[1] Main text.
```

Such markup would also be easier to parse, allowing for the automatic creation of the necessary files for LLMs, or AI systems could generate them more accurately on their own.