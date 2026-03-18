# A compromise between minified and fully indented json.
# Example: {"a":[1,2]} ->
# {
#   "a": [1, 2]
# }
# Which looks better than putting those single digits each on their own line.
import io, json

def json_dumps(obj):
    f = io.StringIO()
    json_dump(obj, f)
    return f.getvalue()

def json_dump(obj, f):
    def indented_dict(obj, indentation):
        f.write("{")
        child_indentation = indentation + "  "
        comma = "\n" + child_indentation
        final_indentation = ""
        for k, v in obj.items():
            f.write(comma)
            f.write(json.dumps(k))
            f.write(": ")
            recurse(v, child_indentation)
            comma = ",\n" + child_indentation
            final_indentation = "\n" + indentation
        f.write(final_indentation)
        f.write("}")
    def indented_list(obj, indentation):
        f.write("[")
        child_indentation = indentation + "  "
        comma = "\n" + child_indentation
        final_indentation = ""
        for v in obj:
            f.write(comma)
            recurse(v, child_indentation)
            comma = ",\n" + child_indentation
            final_indentation = "\n" + indentation
        f.write(final_indentation)
        f.write("]")
    def is_primitive(obj):
        return obj is None or type(obj) in (int, float, bool, str)
    def is_short(obj):
        return obj is None or type(obj) in (int, float, bool)
    def recurse(obj, indentation):
        if type(obj) == dict:
            if len(obj) == 0:
                f.write("{}")
            elif len(obj) == 1 and all(is_primitive(v) for v in obj.values()):
                f.write(json.dumps(obj))
            elif len(obj) == 2 and all(is_short(v) for v in obj.values()):
                f.write(json.dumps(obj))
            elif len(obj) == 1:
                # {"k": {"k": {"k": []}}}
                # {"k": [
                #   ...
                # ]}
                f.write("{")
                [(k, v)] = obj.items()
                f.write(json.dumps(k))
                f.write(": ")
                recurse(v, indentation) # No extra indent.
                f.write("}")
            else:
                indented_dict(obj, indentation)
        elif type(obj) == list:
            if len(obj) == 0:
                f.write("[]")
            elif len(obj) <= 2 and all(is_primitive(v) for v in obj):
                f.write(json.dumps(obj))
            elif len(obj) <= 4 and all(is_short(v) for v in obj):
                f.write(json.dumps(obj))
            elif len(obj) == 1:
                # [{"k": [{"k": []}]}]
                # [{"k": [
                #   ...
                # ]}]
                f.write("[")
                recurse(obj[0], indentation) # No extra indent.
                f.write("]")
            else:
                indented_list(obj, indentation)
        elif is_primitive(obj):
            f.write(json.dumps(obj))
        else:
            assert False, "unsupported type: " + repr(obj)
    recurse(obj, "")
    f.write("\n")
