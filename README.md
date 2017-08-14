# Welcome to Archive Observations project

This program extracts metadata from Gemini Archive. This is just an example and it was 
developed only for educational purposes.

With this proof-of-concept, we want to answer a simple question: Where has Gemini Observatory 
pointed out on the sky in a certain period of time?.


## Requirements

* Python 3.5 (https://www.python.org/)
* Python Version Management: pyenv (https://github.com/pyenv/pyenv)


## Configure

This sample is using a mechanism for isolating Python environment. So, first run the following 
command at the project root:

```bash
> make
```

The above command will install all required dependencies on .venv folder.

Now, you need to active the environment:

```bash
> source .venv/bin/activate
```


## Run

For fetching data from the archive, run:

```bash
> archive_obs -f 2017-05-01 -t 2017-05-15 --fetch
```

Certainly, extract data from a website takes time and we can find several issues, like service 
down or service rejection. So, we provide a set of samples which were taken while this program 
was under development. The sample data raw.zip is online at 
`https://drive.google.com/drive/folders/0B7hGAuX52u9va01WSDZXeWxvVkU?usp=sharing`.
Please, decompress the file into the data `folder`, first make sure there is not another raw 
folder with data.

The parse option take FITS header files in a range of dates and convert them in a CSV 
representation. A CSV file isn't overwritten if it exist.

```bash
> archive_obs -f 2017-05-01 -t 2017-05-15 --parse
```

If you don't provide dates for options `fetch` and `parse`, then they will be set up with values 
of the last night.

Finaly, we can see where Gemini Observatory has been pointing out, running:

```bash
> archive_obs --show
```

This option is taken all collected data from the CSV file. Also, we can store the map as a PDF file
with the opciotn `--save`. There is a sample file called `map.pdf` into the `data` folder


##Testing

Execute at the project root:

```sh
flake8 && py.test
```


## TODO

  * Determinate what means the following prefixs in FITS filename: `gS`, `N`, and `S`. Not all 
  collected data have RA and Dec coordinates.
  * There is a wrong value for date in file N20170504S0265_flat.fits. It says `2017-06-18`, but it
  should be `2017-05-05`.
  * Improve unit tests


Any problem or question about this project, please email me at efulet@gmail.com
