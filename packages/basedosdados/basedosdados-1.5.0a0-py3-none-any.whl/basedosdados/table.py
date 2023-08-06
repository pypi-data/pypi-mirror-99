from jinja2 import Template
from pathlib import Path, PosixPath
import json
import csv
from copy import deepcopy
from google.cloud import bigquery
import datetime

import google.api_core.exceptions

from basedosdados.base import Base
from basedosdados.storage import Storage
from basedosdados.dataset import Dataset
from basedosdados.exceptions import BaseDosDadosException


class Table(Base):
    """
    Manage tables in Google Cloud Storage and BigQuery.
    """

    def __init__(self, table_id, dataset_id, **kwargs):
        super().__init__(**kwargs)

        self.table_id = table_id.replace("-", "_")
        self.dataset_id = dataset_id.replace("-", "_")
        self.dataset_folder = Path(self.metadata_path / self.dataset_id)
        self.table_folder = self.dataset_folder / table_id
        self.table_full_name = dict(
            prod=f"{self.client['bigquery_prod'].project}.{self.dataset_id}.{self.table_id}",
            staging=f"{self.client['bigquery_staging'].project}.{self.dataset_id}_staging.{self.table_id}",
        )
        self.table_full_name.update(dict(all=deepcopy(self.table_full_name)))

    @property
    def table_config(self):
        return self._load_yaml(self.table_folder / "table_config.yaml")

    def _get_table_obj(self, mode):
        return self.client[f"bigquery_{mode}"].get_table(self.table_full_name[mode])

    def _load_schema(self, mode="staging"):
        """Load schema from table_config.yaml

        Args:
            mode (bool): Which dataset to create [prod|staging|all].
        """

        self._check_mode(mode)

        json_path = self.table_folder / f"schema-{mode}.json"
        columns = self.table_config["columns"]

        if mode == "staging":

            new_columns = []
            for c in columns:
                if not c.get("is_partition"):
                    c["type"] = "STRING"
                    new_columns.append(c)

            del columns
            columns = new_columns

        elif mode == "prod":
            schema = self._get_table_obj(mode).schema

            for c in columns:
                for s in schema:
                    if c["name"] == s.name:
                        c["type"] = s.field_type
                        c["mode"] = s.mode
                        break
                else:
                    raise Exception(
                        f"Column {c} was not found in schema. Are you sure that "
                        "all your column names between table_config.yaml and "
                        "publish.sql are the same?"
                    )
        ## force utf-8
        json.dump(columns, (json_path).open("w", encoding="utf-8"))

        return self.client[f"bigquery_{mode}"].schema_from_json(str(json_path))

    def _make_template(self, columns, partition_columns):

        for file in (Path(self.templates) / "table").glob("*"):

            if file.name in ["table_config.yaml", "publish.sql"]:

                # Load and fill template
                template = Template(file.open("r", encoding="utf-8").read()).render(
                    bucket_name=self.bucket_name,
                    table_id=self.table_id,
                    dataset_id=self.dataset_folder.stem,
                    project_id=self.client["bigquery_staging"].project,
                    project_id_prod=self.client["bigquery_prod"].project,
                    columns=columns,
                    partition_columns=partition_columns,
                    now=datetime.datetime.now().strftime("%Y-%m-%d"),
                )

                # Write file
                (self.table_folder / file.name).open("w", encoding="utf-8").write(
                    template
                )

    def init(
        self,
        data_sample_path=None,
        if_folder_exists="raise",
        if_table_config_exists="raise",
    ):
        """Initialize table folder at metadata_path at `metadata_path/<dataset_id>/<table_id>`.

        The folder should contain:

        * `table_config.yaml`
        * `publish.sql`

        You can also point to a sample of the data to auto complete columns names.

        Args:
            data_sample_path (str, pathlib.PosixPath): Optional.
                Data sample path to auto complete columns names
                It supports Comma Delimited CSV.
            if_folder_exists (str): Optional.
                What to do if table folder exists

                * 'raise' : Raises FileExistsError
                * 'replace' : Replace folder
                * 'pass' : Do nothing
            table_config_exists (str): Optional
                What to do if table_config.yaml and publish.sql exists

                * 'raise' : Raises FileExistsError
                * 'replace' : Replace files with blank template
                * 'pass' : Do nothing
        Raises:
            FileExistsError: If folder exists and replace is False.
            NotImplementedError: If data sample is not in supported type or format.
        """
        if not self.dataset_folder.exists():

            raise FileExistsError(
                f"Dataset folder {self.dataset_folder} folder does not exists. "
                "Create a dataset before adding tables."
            )

        try:
            self.table_folder.mkdir(exist_ok=(if_folder_exists == "replace"))
        except FileExistsError:
            if if_folder_exists == "raise":
                raise FileExistsError(
                    f"Table folder already exists for {self.table_id}. "
                )
            elif if_folder_exists == "pass":
                return self

        if not data_sample_path and if_table_config_exists != "pass":
            raise BaseDosDadosException(
                "You must provide a path to correctly create config files"
            )

        partition_columns = []
        if isinstance(
            data_sample_path,
            (
                str,
                Path,
            ),
        ):
            # Check if partitioned and get data sample and partition columns
            data_sample_path = Path(data_sample_path)

            if data_sample_path.is_dir():

                data_sample_path = [
                    f
                    for f in data_sample_path.glob("**/*")
                    if f.is_file() and f.suffix == ".csv"
                ][0]

                partition_columns = [
                    k.split("=")[0]
                    for k in data_sample_path.as_posix().split("/")
                    if "=" in k
                ]

            if data_sample_path.suffix == ".csv":

                columns = next(
                    csv.reader(open(data_sample_path, "r", encoding="utf-8"))
                )

            else:
                raise NotImplementedError(
                    "Data sample just supports comma separated csv files"
                )

        else:

            columns = ["column_name"]

        if if_table_config_exists == "pass":
            # Check if config files exists before passing
            if (
                Path(self.table_folder / "table_config.yaml").is_file()
                and Path(self.table_folder / "publish.sql").is_file()
            ):
                pass
            # Raise if no sample to determine columns
            elif not data_sample_path:
                raise BaseDosDadosException(
                    "You must provide a path to correctly create config files"
                )
            else:
                self._make_template(columns, partition_columns)

        elif if_table_config_exists == "raise":

            # Check if config files already exist
            if (
                Path(self.table_folder / "table_config.yaml").is_file()
                and Path(self.table_folder / "publish.sql").is_file()
            ):

                raise FileExistsError(
                    f"table_config.yaml and publish.sql already exists at {self.table_folder}"
                )
            # if config files don't exist, create them
            else:
                self._make_template(columns, partition_columns)

        else:
            # Raise: without a path to data sample, should not replace config files with empty template
            self._make_template(columns, partition_columns)

        return self

    def create(
        self,
        path=None,
        job_config_params=None,
        partitioned=False,
        force_dataset=True,
        if_table_exists="raise",
        if_storage_data_exists="raise",
        if_table_config_exists="raise",
    ):
        """Creates BigQuery table at staging dataset.

        If you add a path, it automatically saves the data in the storage,
        creates a datasets folder and BigQuery location, besides creating the
        table and its configuration files.

        The new table should be located at `<dataset_id>_staging.<table_id>` in BigQuery.

        It looks for data saved in Storage at `<bucket_name>/staging/<dataset_id>/<table_id>/*`
        and builds the table.

        It currently supports the types:
            - Comma Delimited CSV

        Data can also be partitioned following the hive partitioning scheme
        `<key1>=<value1>/<key2>=<value2>`, for instance, `year=2012/country=BR`

        Args:
            path (str or pathlib.PosixPath): Where to find the file that you want to upload to create a table with
            job_config_params (dict): Optional.
                Job configuration params from bigquery
            partitioned (bool): Optional.
                Whether data is partitioned
            if_table_exists (str): Optional
                What to do if table exists

                * 'raise' : Raises Conflict exception
                * 'replace' : Replace table
                * 'pass' : Do nothing
            force_dataset (bool): Creates `<dataset_id>` folder and BigQuery Dataset if it doesn't exists.
            if_table_config_exists (str): Optional.
                 What to do if config files already exist

                 * 'raise': Raises FileExistError
                 * 'replace': Replace with blank template
                 * 'pass'; Do nothing
            if_storage_data_exists (str): Optional.
                What to do if data already exists on your bucket:

                * 'raise' : Raises Conflict exception
                * 'replace' : Replace table
                * 'pass' : Do nothing

        Todo:

            * Implement if_table_exists=raise
            * Implement if_table_exists=pass
        """

        if path is None:

            # Look if table data already exists at Storage
            data = self.client["storage_staging"].list_blobs(
                self.bucket_name, prefix=f"staging/{self.dataset_id}/{self.table_id}"
            )

            # Raise: Cannot create table without external data
            if not data:
                raise BaseDosDadosException(
                    "You must provide a path for uploading data"
                )

        # Add data to storage
        if isinstance(
            path,
            (
                str,
                Path,
            ),
        ):

            Storage(self.dataset_id, self.table_id, **self.main_vars).upload(
                path, mode="staging", if_exists=if_storage_data_exists
            )

        # Create Dataset if it doesn't exist
        if force_dataset:

            dataset_obj = Dataset(self.dataset_id, **self.main_vars)

            try:
                dataset_obj.init()
            except FileExistsError:
                pass

            dataset_obj.create(if_exists="pass")

        self.init(
            data_sample_path=path,
            if_folder_exists="replace",
            if_table_config_exists=if_table_config_exists,
        )

        external_config = external_config = bigquery.ExternalConfig("CSV")
        external_config.options.skip_leading_rows = 1
        external_config.options.allow_quoted_newlines = True
        external_config.options.allow_jagged_rows = True
        external_config.autodetect = False
        external_config.schema = self._load_schema("staging")

        external_config.source_uris = (
            f"gs://{self.bucket_name}/staging/{self.dataset_id}/{self.table_id}/*"
        )

        if partitioned:

            hive_partitioning = bigquery.external_config.HivePartitioningOptions()
            hive_partitioning.mode = "AUTO"
            hive_partitioning.source_uri_prefix = self.uri.format(
                dataset=self.dataset_id, table=self.table_id
            ).replace("*", "")
            external_config.hive_partitioning = hive_partitioning

        table = bigquery.Table(self.table_full_name["staging"])

        table.external_data_configuration = external_config
        # Lookup if table alreay exists
        table_ref = None
        try:
            table_ref = self.client["bigquery_staging"].get_table(
                self.table_full_name["staging"]
            )

        except google.api_core.exceptions.NotFound:
            pass

        if isinstance(table_ref, google.cloud.bigquery.table.Table):

            if if_table_exists == "pass":

                return None

            elif if_table_exists == "raise":

                raise FileExistsError(
                    "Table already exists, choose replace if you want to overwrite it"
                )

        if if_table_exists == "replace":

            self.delete(mode="staging")

        self.client["bigquery_staging"].create_table(table)

    def update(self, mode="all", not_found_ok=True):
        """Updates BigQuery schema and description.

        Args:
            mode (str): Optional.
                Table of which table to update [prod|staging|all]
            not_found_ok (bool): Optional.
                What to do if table is not found
        """

        self._check_mode(mode)

        if mode == "all":
            mode = ["prod", "staging"]
        else:
            mode = [mode]

        for m in mode:

            try:
                table = self._get_table_obj(m)
            except google.api_core.exceptions.NotFound:
                continue

            table.description = self._render_template(
                Path("table/table_description.txt"), self.table_config
            )

            # save table description
            open(
                self.metadata_path
                / self.dataset_id
                / self.table_id
                / "table_description.txt",
                "w",
                encoding="utf-8",
            ).write(table.description)

            # if m == "prod":/
            table.schema = self._load_schema(m)

            self.client[f"bigquery_{m}"].update_table(
                table, fields=["description", "schema"]
            )

    def publish(self, if_exists="raise"):
        """Creates BigQuery table at production dataset.

        Table should be located at `<dataset_id>.<table_id>`.

        It creates a view that uses the query from
        `<metadata_path>/<dataset_id>/<table_id>/publish.sql`.

        Make sure that all columns from the query also exists at
        `<metadata_path>/<dataset_id>/<table_id>/table_config.sql`, including
        the partitions.

        Args:
            if_exists (str): Optional.
                What to do if table exists.

                * 'raise' : Raises Conflict exception
                * 'replace' : Replace table
                * 'pass' : Do nothing

        Todo:

            * Check if all required fields are filled
        """

        if if_exists == "replace":
            self.delete(mode="prod")

        self.client["bigquery_prod"].query(
            (self.table_folder / "publish.sql").open("r", encoding="utf-8").read()
        ).result()

        self.update("prod")

    def delete(self, mode):
        """Deletes table in BigQuery.

        Args:
            mode (str): Table of which table to delete [prod|staging|all]
        """

        self._check_mode(mode)

        if mode == "all":
            for m, n in self.table_full_name[mode].items():
                self.client[f"bigquery_{m}"].delete_table(n, not_found_ok=True)
        else:
            self.client[f"bigquery_{mode}"].delete_table(
                self.table_full_name[mode], not_found_ok=True
            )

    def append(self, filepath, partitions=None, if_exists="raise", **upload_args):
        """Appends new data to existing BigQuery table.

        As long as the data has the same schema. It appends the data in the
        filepath to the existing table.

        Args:
            filepath (str or pathlib.PosixPath): Where to find the file that you want to upload to create a table with
            partitions (str, pathlib.PosixPath, dict): Optional.
                Hive structured partition as a string or dict

                * str : `<key>=<value>/<key2>=<value2>`
                * dict: `dict(key=value, key2=value2)`
            if_exists (str): 0ptional.
                What to do if data with same name exists in storage

                * 'raise' : Raises Conflict exception
                * 'replace' : Replace table
                * 'pass' : Do nothing
        """

        Storage(self.dataset_id, self.table_id, **self.main_vars).upload(
            filepath,
            mode="staging",
            partitions=None,
            if_exists=if_exists,
            **upload_args,
        )

        self.create(
            if_table_exists="replace",
            if_table_config_exists="pass",
            if_storage_data_exists="pass",
        )
