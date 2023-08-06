<img align="left" src="https://desycloud.desy.de/index.php/s/mWtE987dgK4NdFc/preview" width="150" height="150"/>  
<br>

# Alert support for AMPEL

<br><br>

This add-on enables the processing of `alerts` by AMPEL.
The central class of this repository, `ampel.alert.AlertProcessor`,
is capable of `loading`, `filtering`, `ingesting` these alerts.

- The loading part involves system (or instrument) specific classes.
- The optional filtering part allows the selection of events based on pre-defined rules. 
High-throughput systems, such as ZTF or LSST in astronomy, rely on such filters.
- The `ingestion` is the step where the content of alerts is saved into the AMPEL database, possibly along with different other documents which can be created according to pre-defined directives.

<p align="center">
  <img src="https://desycloud.desy.de/index.php/s/fiLRCFZtbTkeCtj/preview" width="40%" />
  <img src="https://desycloud.desy.de/index.php/s/EBacs5bbApzpwDr/preview" width="40%" />  
</p>

<p align="center">
  The <i>AlertProcessor</i> operates on the first three tiers of AMPEL: T0, T1 and T2.
</p>


## Loading Alert 

Performed by subclasses of `ampel.abstract.AbsAlertSupplier`.

Concrete implementation examples: `ampel.ztf.alert.ZiAlertSupplier`

Actions break-down:

- Load bytes (tar, network, ...)
- Deserialize (avro, bson, json, ...)
- First shape (instrument specific): morph into `AmpelAlert` or `PhotoAlert` Purpose: having a common format that the `AlertProcessor` and alert filters understand. A `PhotoAlert` typically contains two distinct flat sequences, one for photopoints and one for upperlimits. The associated object ID, such as the ZTF name, is converted into nummerical ampel IDs. This is necessary for all alerts (rejected one as well) since "autocomplete" is based on true Ampel IDs.


## Filtering Alert 

Filtering alerts is performed per channel by subclasses of `ampel.abstract.AbsAlertFilter`.
An `AlertProcessor` instance can handle multiple filters.
Alert filters methods provided by user units are called by the class `FilterBlock`,
that handles associated operations (what happens to rejected alerts ? what about auto-complete, etc...) 
`FilterBlock` instances are themselves embedded in `FilterBlocksHandler`

Filters can return:
  - `False` or `None` to reject an alert.
  - `True` to accept the alert and create all t1/t2 documents defined in the alert processor directive
  - An `int` number to accept the alert and create only the t1/t2 documents associated with this group id (as defined in the alert processor directive)

## Ingesting Alert 

If any channel accepts a given alert, DB updates need to occur.
v0.7 brought many updates regarding how ingestion happens.
Class: `ampel.alert.IngestionHandler`, `ampel.abstract.ingest.AbsIngester`

More details later

### Directives
Nesting is chaining

### Second shape: morph into `DataPoint`

Alerts that pass any T0 filter are further shaped in order to fullfill
some requirements for DB storage and easy later retrieval.
Among other things, individual datapoints can be tagged during this step.
For ZTF, upper limits do not feature a unique ID, so we have to build our own.
Each datapoint is shaped into a `ampel.content.DataPoint` structure.

Implementation example: `ampel.ztf.ingest.ZiT0PhotoPointShaper`

### Compilers
Optimize the number of created documents

### Ingesters
Create and upserts documents into the DB
