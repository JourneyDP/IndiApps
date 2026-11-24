"""IndiApps core v0.1 validator (DRAFT).

Checks a pack against the JSON Schema, then applies the cross-reference rules
the schema cannot express. Also runs the conformance cases.

Usage:
    python validate_pack.py pack.json            # validate one pack
    python validate_pack.py --cases cases.json   # run conformance cases
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).with_name("indiapps-core-v0.1.schema.json")
SCHEMA = json.loads(SCHEMA_PATH.read_text())


def schema_errors(doc, def_name):
    schema = {"$schema": SCHEMA["$schema"], "$ref": f"#/$defs/{def_name}", "$defs": SCHEMA["$defs"]}
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"schema: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}" for e in v.iter_errors(doc)]


def pack_rule_errors(pack):
    """Cross-reference rules R1 to R8 from the charter."""
    errs = []
    dims = {d["dimensionId"] for d in pack["dimensions"]}
    units = {u["unitId"]: u["dimensionId"] for u in pack["units"]}
    rtypes = {r["resourceTypeId"]: set(r["dimensions"]) for r in pack["resourceTypes"]}

    def dupes(ids, what):
        seen = set()
        for i in ids:
            if i in seen:
                errs.append(f"R1: duplicate {what} id '{i}'")
            seen.add(i)

    dupes([d["dimensionId"] for d in pack["dimensions"]], "dimension")
    dupes([u["unitId"] for u in pack["units"]], "unit")
    dupes([r["resourceTypeId"] for r in pack["resourceTypes"]], "resource type")
    dupes([w["workflowId"] for w in pack["workflows"]], "workflow")

    for u, d in units.items():
        if d not in dims:
            errs.append(f"R2: unit '{u}' uses unknown dimension '{d}'")
    for r in pack["resourceTypes"]:
        for d in r["dimensions"]:
            if d not in dims:
                errs.append(f"R3: resource type '{r['resourceTypeId']}' uses unknown dimension '{d}'")
        for rule in r.get("consumptionRules", []):
            if rule["dimensionId"] not in r["dimensions"]:
                errs.append(f"R3: rule '{rule['ruleId']}' uses a dimension its resource type does not declare")
    for c in pack.get("conversions", []):
        f, t = c["fromUnit"], c["toUnit"]
        if f not in units or t not in units:
            errs.append(f"R4: conversion {f}->{t} uses an unknown unit")
        elif units[f] != units[t] and "resourceTypeId" not in c:
            errs.append(f"R4: conversion {f}->{t} crosses dimensions without naming a resource type")
        if c.get("resourceTypeId") and c["resourceTypeId"] not in rtypes:
            errs.append(f"R4: conversion {f}->{t} names unknown resource type '{c['resourceTypeId']}'")
    for w in pack["workflows"]:
        node_ids = [n["nodeId"] for n in w["nodes"]]
        dupes(node_ids, f"node in workflow '{w['workflowId']}'")
        if w.get("startNode") and w["startNode"] not in node_ids:
            errs.append(f"R5: workflow '{w['workflowId']}' startNode is not one of its nodes")
        for n in w["nodes"]:
            for nxt in n.get("next", []):
                if nxt not in node_ids:
                    errs.append(f"R5: node '{n['nodeId']}' points to unknown node '{nxt}'")
            for fl in n.get("flows", []):
                rt = fl["resourceTypeId"]
                if rt not in rtypes:
                    errs.append(f"R6: node '{n['nodeId']}' uses unknown resource type '{rt}'")
                    continue
                q = fl.get("quantity")
                if q:
                    if q["unit"] not in units:
                        errs.append(f"R7: node '{n['nodeId']}' uses unknown unit '{q['unit']}'")
                    elif units[q["unit"]] not in rtypes[rt]:
                        errs.append(
                            f"R7: node '{n['nodeId']}' counts '{rt}' in '{q['unit']}', "
                            f"a dimension that resource type does not allow"
                        )
    cap = pack["policies"]["moneyCapPerAction"]
    if units.get(cap["unit"]) != "currency":
        errs.append("R8: moneyCapPerAction must be in a unit of the 'currency' dimension")
    if cap["value"] < 0:
        errs.append("R8: moneyCapPerAction cannot be negative")
    return errs


def validate(doc, def_name="Pack"):
    errs = schema_errors(doc, def_name)
    if not errs and def_name == "Pack":
        errs = pack_rule_errors(doc)
    return errs


def run_cases(path):
    cases = json.loads(Path(path).read_text())["cases"]
    failed = 0
    for c in cases:
        errs = validate(c["doc"], c["def"])
        ok = (not errs) == c["valid"]
        if ok and not c["valid"] and c.get("expect") and not any(c["expect"] in e for e in errs):
            ok = False
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {c['id']}  ({'valid' if c['valid'] else 'invalid'}) {c['title']}")
        if not ok or (errs and "-v" in sys.argv):
            for e in errs:
                print("      ", e)
    print(f"\n{len(cases) - failed} of {len(cases)} cases passed")
    return failed


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--cases":
        sys.exit(1 if run_cases(sys.argv[2]) else 0)
    problems = validate(json.loads(Path(sys.argv[1]).read_text()))
    print("\n".join(problems) or "OK")
    sys.exit(1 if problems else 0)
