# Anki-Sync

Anki-Sync enables bulk-modifications and creation of flashcards.
Its capabilities include modifying, extending, and transferring flashcards using external providers.

## Requirements

Anki-Sync requires python3 to run.
Additionally, software listed in `requirements.txt` will have to be installed for the system to function properly.
The recommended installation method is by using virtual-environments or conda, but a global `pip install` would work as well.

Additionally, certain endpoints require additional configuration:

 * Anki: Anki requires [Anki-Connect](https://github.com/FooSoft/anki-connect) installed and running on the local system. A restart of Anki will be required after installing the plugin.

## Installation

### Check if python is installed

First, check if Python is already installed on your system by running the following command in your terminal:

```bash
python3 --version
```

If Python is installed, you should see something like this:

```
Python 3.10.9
```

If Python is not installed, you can install it by following the next step.

### Install python

To install Python3 on your system, open your terminal and enter the following command:

```bash
sudo apt-get install python3
```

This will install Python3 on your system.

### Install Virtualenv

Next, you'll need to install Virtualenv, a tool for creating isolated Python environments.
You can do this by running the following command in your terminal:

```bash
sudo apt-get install virtualenv
```

### Create a Virtual Environment

Now that you have Virtualenv installed, you can create a virtual environment for the Python project.
To do this, navigate to the directory where you want to create your environment and run the following command:

```bash
virtualenv venv
```

This will create a new virtual environment called "venv" in the current directory.

### Activate the Virtual Environment

To activate your new virtual environment, run the following command:

```bash
source venv/bin/activate
```

You should see your terminal prompt change to indicate that you are now in your virtual environment.

### Install Packages

Now that you're in your virtual environment, you can install any packages you need for your project using pip.
To install all currently required packages, you can run the following command:

```bash
pip install -r requirements.txt
```

## Endpoints

Following is a table of what default endpoints are currently available, and which kind of manipulation they can be used for:

| Name           | NoteProvider | NoteConsumer | BaseProvider |
|----------------|--------------|--------------|--------------|
| Anki           | Yes          | Yes          | No           |
| Jisho          | No           | No           | Yes          |
| Wanikani       | Yes          | No           | Yes          |
| split          | No           | No           | Yes          |
| replace_prefix | No           | No           | Yes          |
| replace_suffix | No           | No           | Yes          |
| replace        | No           | No           | Yes          |

 * NoteProvider: Allows the system to read notes from the specific source
 * NoteConsumer: Allows the system to store or update notes to the specific source
 * BaseProvider: Enhances notes by modifying or updating information

## Configuration

This project uses a single `settings.json` file as it's main source for configuration.
The file is separated in two sections; `endpoints` and `config`.
```json
{
  "endpoints": {},
  "config": []
}
```

### Endpoints

Endpoints contain the general endpoint configuration.
Each endpoint will be referenced by name at least once for it to be considered enabled.
Even an empty object will cause the endpoint to be active, but some might require a bit more to be any kind of use.

#### Wanikani

```json
{
  "wanikani": {
    "api_token": "<The api token from https://www.wanikani.com/settings/personal_access_tokens>"
  }
}
```

#### Anki

```json
{
  "anki": {
    "target_deck": "<Target Anki-Deck name>"
  }
}
```

#### Jisho

```json
{
  "jisho": {}
}
```

#### Replace Prefix

```json
{
  "replace_prefix": {
    "source_field": "Question",
    "search_string": "<Prefix to be removed>",
    "replacement_string": "<replacement or empty string>"
  }
}
```

#### Replace Suffix

```json
{
  "replace_suffix": {
    "source_field": "Question",
    "search_string": "<Suffix to be removed>",
    "replacement_string": "<replacement or empty string>"
  }
}
```

#### Replace

```json
{
  "replace": {
    "source_field": "Question",
    "search_string": "<String to be removed>",
    "replacement_string": "<replacement or empty string>"
  }
}
```

#### Split

```json
{
  "split": {
    "source_field": "Question",
    "search_string": "<String to split by. Only first occurrence will be used>",
    "target_field_left": "<Field to store the left part of the string>",
    "target_field_right": "<Field to store the right part of the string>"
  }
}
```

### Config

The config section configures the synchronization steps to be taken.
Each step consists of a provider (source) and a consumer (target).
Notes are initially loaded from the provider, modified and enhanced by the providers listed in enrichment and stored to the consumer.
The source and target may be the same endpoint, to allow for update scenarios.

__Adding Wanikani Information to notes__

```json
[
  {
      "source": "anki",
      "target": "anki",
      "enrichment": [
        "wanikani"
      ]
    }
]
```

__Importing vocabulary from Wanikani into anki__

```json
{
  "source": "wanikani",
  "target": "anki"
}
```

__Cleaning and separating input__

This scenario assumes a Question in the following pattern:
`<ruby>Kanji<rt>Hiragana</rt></ruby>`
Which is the format sometimes used in the official Genki Notes.
It separates the Kanji and Hiragana parts into two separate fields.

```json
{
  "source": "anki",
  "target": "anki",
  "example": "口<rt>くち",
  "enrichment": [
    "replace_prefix",
    "replace_suffix",
    "split"
  ]
}
```