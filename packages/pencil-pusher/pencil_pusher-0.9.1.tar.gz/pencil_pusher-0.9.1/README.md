# pencil_pusher ✏️
pencil_pusher: A Github Action that creates and publishes source documentation to the repository's wiki.

# Tech Stack
- :whale: docker
- python
- [pydoc-markdown](https://pydoc-markdown.readthedocs.io/en/latest/)

# Inputs

| Input Name            | Type     | Required | Default                 | Description                                                                                                                                                             |
|-----------------------|----------|----------|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| owner_name            | `string` | `true`   | `None`                  | The username of the repository owner                                                                                                                                    |
| repository_name       | `string` | `true`   | `None`                  | The name of the repository being accessed                                                                                                                               |
| personal_access_token | `string` | `true`   | `None`                  | A [github personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) with full repository permissions checked. |
| config_file           | `string` | `false`  | `"./pencil_pusher.config.json"` | This is the location of the config file. The config file is where you define which source files should be documented and how they should map to individual wiki pages.  |

# Config File
This action requires that the calling repository define a file called `pencil_pusher.config.json` where the auto doc generator can process which source files to document and how to map those source files to wiki pages. 

Here is the format
```json
{
  "languages": ["python"],
  "sources": [
    "mypackage/mymodule1/myfile1.py",
    "mypackage/mymodule2/"
  ],
  "title_prefix": "MyPackage",
  "title_suffix": "API",
  "titles": [
    {
      "source_file": "mypackage/mymodule1/myfile1.py",
      "title": "Utilities",
      "use_prefix": true,
      "use_suffix": false
    }
  ]
}

```

| Config | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | 
| languages | `Array<string>` | `true` | `["python"]` | All the languages to process for documentation (currently only python is supported) | 
| sources | `Array<string>` | `true` | `[]` | relative locations to the root of the project of source files to process for documentation. This can be both files and directories. | 
| title_prefix | `string` | `false` | `""` | The text to be appended to the front of each title for each source file wiki doc generated | 
| title_suffix | `string` | `false` | `""` | The text to be appended to the back of each title for each source file wiki doc generated | 
| titles | `Array<json>` | `false` | `[]` | A dictionary for defining custom titles to be generated | 
| titles.source_file | `string` | `true` | `""` | the relative location of the source file being given a custom title (must be a file) |
| titles.title | `string` | `false` | `""` | replacement title to use for this source file | 
| titles.use_prefix | `string` | `false` | `""` | flag if prefix defined above should be used in this title (will be ommitted if `title_prefix` is not defined) | 
| titles.use_suffix | `string` | `false` | `""` | flag if suffix defined above should be used in this title (will be ommitted if `titel_suffix` is not defined) |


