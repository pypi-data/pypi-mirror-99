"""Import from internal location"""
import cgi
import datetime
import grp
import json
import mimetypes
import os
import pathlib
import pwd
import shutil
import tempfile

from ckan import logic

import dclab
from dcor_shared import get_resource_path

from .orgs import INTERNAL_ORG
from .paths import INTERNAL_DEPOT
from .depot import DUMMY_BYTES, make_id


def admin_context():
    return {'ignore_auth': True, 'user': 'default'}


def create_internal_org():
    """Creates a CKAN organization (home of all linked data)"""
    organization_show = logic.get_action("organization_show")
    organization_create = logic.get_action("organization_create")
    # check if organization exists
    try:
        organization_show(context=admin_context(),
                          data_dict={"id": INTERNAL_ORG})
    except logic.NotFound:
        # create user
        data_dict = {
            "name": INTERNAL_ORG,
            "description": u"Internal/archived datasets of the Guck "
            + u"division. All datasets are private. If you are "
            + u"missing a dataset, please contact Paul Müller.",
            "title": "Guck Division Archive"
        }
        organization_create(context=admin_context(),
                            data_dict=data_dict)


def load_sha256sum(path):
    stem = "_".join(path.name.split("_")[:3])
    sha256path = path.with_name(stem + ".sha256sums")
    try:
        sums = sha256path.read_text().split("\n")
    except UnicodeDecodeError:
        print("DAMN! Bad character in {}!".format(sha256path))
        raise
    for line in sums:
        line = line.strip()
        if line:
            ss, name = line.split("  ")
            if name == path.name:
                return ss
    else:
        raise ValueError("Could not find sha256 sum for {}!".format(path))


def import_dataset(sha256_path):
    # determine all relevant resources
    root = sha256_path.parent
    files = sorted(root.glob(sha256_path.name.split(".")[0]+"*"))

    for ff in files:
        if ff.name.count("_condensed"):
            fc = ff
            break
    else:
        raise ValueError("No condensed file for {}!".format(sha256_path))

    if len(files) > 50:
        raise ValueError("Found too many ({}) files for {}!".format(
            len(files), sha256_path))

    files = [ff for ff in files if not ff.name.count("_condensed")]
    files = [ff for ff in files if not ff.suffix == ".sha256sums"]

    for ff in files:
        if ff.suffix == ".rtdc":
            break
    else:
        raise ValueError("No dataset file for {}!".format(sha256_path))

    # create the dataset
    dcor_dict = make_dataset_dict(ff)

    package_show = logic.get_action("package_show")
    package_create = logic.get_action("package_create")
    try:
        package_show(context=admin_context(),
                     data_dict={"id": dcor_dict["name"]})
    except logic.NotFound:
        package_create(context=admin_context(), data_dict=dcor_dict)
    else:
        print("Skipping creation of {} (exists) ".format(dcor_dict["name"]),
              end="\r")

    resource_show = logic.get_action("resource_show")
    resource_create = logic.get_action("resource_create")
    rmid = make_id([dcor_dict["id"], ff.name, load_sha256sum(ff)])
    try:
        resource_show(context=admin_context(), data_dict={"id": rmid})
    except logic.NotFound:
        # make link to condensed  before importing the resource
        # (to avoid conflicts with automatic generation of condensed file)
        rmpath = get_resource_path(rmid, create_dirs=True)
        # This path should not exist (checked above)
        rmpath_c = rmpath.with_name(rmpath.name + "_condensed.rtdc")
        assert not rmpath_c.exists(), "Should not exist: {}".format(rmpath_c)
        rmpath_c.symlink_to(fc)

        # import the resources
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="import_"))
        for path in files:
            print("  - importing {}".format(path))
            # use dummy file (workaround for MemoryError during upload)
            upath = tmp / path.name
            with upath.open("wb") as fd:
                fd.write(DUMMY_BYTES)
            shasum = load_sha256sum(path)
            with upath.open("rb") as fd:
                # This is a kind of hacky way of tricking CKAN into thinking
                # that there is a file upload.
                upload = cgi.FieldStorage()
                upload.filename = path.name  # used in ResourceUpload
                upload.file = fd  # used in ResourceUpload
                upload.list.append(None)  # for boolean test in ResourceUpload
                rs = resource_create(
                    context=admin_context(),
                    data_dict={
                        "id": make_id([dcor_dict["id"],
                                       path.name,
                                       load_sha256sum(path)]),
                        "package_id": dcor_dict["name"],
                        "upload": upload,
                        "name": path.name,
                        "sha256": shasum,
                        "size": path.stat().st_size,
                        "format": mimetypes.guess_type(str(path))[0],
                    }
                )
            rpath = get_resource_path(rs["id"])
            rpath.unlink()
            rpath.symlink_to(path)
            # make www-data the owner of the resource
            www_uid = pwd.getpwnam("www-data").pw_uid
            www_gid = grp.getgrnam("www-data").gr_gid
            os.chown(rpath.parent, www_uid, www_gid)
            os.chown(rpath.parent.parent, www_uid, www_gid)
        # activate the dataset
        package_revise = logic.get_action("package_revise")
        package_revise(context=admin_context(),
                       data_dict={"match": {"id": dcor_dict["id"]},
                                  "update": {"state": "active"}})
        # cleanup
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        print("Skipping resource for {} (exists)".format(
              dcor_dict["name"]), end="\r")


def internal(limit=0, start_date="2000-01-01", end_date="3000-01-01"):
    """Import internal datasets

    Parameters
    ----------
    limit: int
        Limit the number of datasets to be imported; If set to 0
        (default), all datasets are imported.
    start_date: str
        Only import datasets in the depot at or after this date
        (format YYYY-MM-DD)
    end_date: str
        Only import datasets in the depot at or before this date
    """
    # prerequisites
    create_internal_org()
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    # iterate through all files
    ii = 0
    for ppsha in pathlib.Path(INTERNAL_DEPOT).rglob("*.sha256sums"):
        # Check whether the date matches
        ppdate = datetime.datetime.strptime(ppsha.name[:10], "%Y-%m-%d")
        if ppdate >= start and ppdate <= end:
            ii += 1
            import_dataset(ppsha)
            if limit and ii >= limit:
                break


def make_dataset_dict(path):
    dcor = {}
    dcor["owner_org"] = INTERNAL_ORG
    dcor["private"] = True
    dcor["license_id"] = "none"
    stem = "_".join(path.name.split("_")[:3])
    dcor["name"] = stem
    dcor["state"] = "active"
    dcor["organization"] = {"id": INTERNAL_ORG}

    with dclab.new_dataset(path) as ds:
        # get the title from the logs
        log = "\n".join(ds.logs["dcor-history"])

    info = json.loads(log)
    op = info["v1"]["origin"]["path"]
    dirs = op.split("/")
    for string in ["Online", "Offline", "online", "offline"]:
        if string in dirs:
            dirs.remove(string)

    dirs[-1] = dirs[-1].rsplit(".", 1)[0]  # remove suffix
    dcor["title"] = " ".join([d.replace("_", " ") for d in dirs])
    # guess author
    dcor["authors"] = "unknown"

    dcor["notes"] = "The location of the original dataset is {}.".format(op)
    dcor["id"] = make_id([load_sha256sum(path), dcor["name"]])
    return dcor
