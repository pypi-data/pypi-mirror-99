from __future__ import absolute_import, division, unicode_literals

from mo_parsing.engine import Engine
from mo_parsing.helpers import delimitedList, restOfLine
from moz_sql_parser.windows import sortColumn, window

from .keywords import *
from .dialects import load_dialect_module
from .clean import strip_comments, encapsulate_variables, pad_comparisons, ENCODING_CHARACTER

HINT_STRING = "__"


def parse_query(query, sql_dialect, feature_name=None) -> tuple:
    """

    :param query:
    :param sql_dialect:
    :param feature_name:
    :return:
    """
    dialect = load_dialect_module(dialect_name=sql_dialect)
    standardized_query = strip_comments(query=query)
    standardized_query = pad_comparisons(query = standardized_query)
    standardized_query, variables = encapsulate_variables(
        query=standardized_query, encoding_character='', wrap_character=ENCODING_CHARACTER,
        skip_characters=0, encoded=False, feature_name=feature_name
    )
    query_ast = dialect.parse_query(query=standardized_query)
    query_input = label_input(variable_set=variables, query_ast=query_ast)

    output = label_output(query_ast=query_ast)
    dependencies = []
    return query_ast, query_input, output, dependencies


def label_input(variable_set, query_ast):
    """

    :param variable_set:
    :param query_ast:
    :return:
    """
    import json
    import re
    variables = dict()

    for group in variable_set:
        for variable in re.findall('(\{[\S]+?\})', group):
            if variable not in variables.keys():
                allows_list = False
                data_type = None
                default_value = None
                clean_name = variable.replace('{', "").replace('}', '')
                display_name = clean_name
                variable_pieces = clean_name.split(HINT_STRING)
                if len(variable_pieces) == 4:
                    display_name = variable_pieces[0]
                    data_type = variable_pieces[1]
                    default_value = json.loads(variable_pieces[2])
                    if variable_pieces[3] == 'true':
                        allows_list = True
                    if default_value == '':
                        default_value = None
                location, found, partial_string = locate_string(s=variable, json=query_ast)
                variables[variable] = dict(
                    name=clean_name, display_name=display_name.split('.')[-1], default_value=default_value,
                    type=data_type, allows_list=allows_list, full_string=group,
                    locations=location,
                    partial_string=partial_string
                )
    return list(variables.values())


def locate_string(s, json):
    location = dict()
    found = False
    partial_string = False
    if isinstance(json, list):
        for idx, v in enumerate(json):
            l, f, p = locate_string(s, v)
            if f:
                location[idx] = l
                found = True
                if p:
                    partial_string = True
    elif isinstance(json, dict):
        for k, v in json.items():
            l, f, p = locate_string(s, v)
            if f:
                location[k] = l
                found = True
                if p:
                    partial_string = True
    elif isinstance(json, str):
        if s in json:
            found = True
            if s != json:
                partial_string = True
    return location, found, partial_string


def label_output(query_ast: dict):
    import json
    outputs = list()
    for idx, column in enumerate(get_select_columns(find_first_node(node_key='select', parse_result=query_ast))):
        display_name = column
        column_pieces = column.split(HINT_STRING)
        is_nullable = True
        data_type = 'string'
        if len(column_pieces) == 3:
            display_name = column_pieces[0]
            data_type = column_pieces[1]
            is_nullable = json.loads(column_pieces[2])
        output = dict(
            display_name=display_name.split('.')[-1],
            index=idx,
            name=column,
            is_nullable=is_nullable,
            type=data_type
        )
        outputs.append(output)
    return outputs


def get_select_columns(select):
    """
    This function searches the given parsed select dictionary to return list of output columns
    :param select: (dict) The select portion of a select statement.
    """
    result = []

    def extract_column_name(i):
        names = []

        if isinstance(i, str):
            names.append(i)
        elif isinstance(i, dict):
            if 'name' in i.keys():
                names.append(i['name'])
            elif 'literal' in i.keys():
                names.append(i['literal'])
            elif 'value' in i.keys():
                names += extract_column_name(i['value'])
            else:
                names += extract_column_name(list(i.values())[0])
        elif isinstance(i, list):
            for x in i:
                n = extract_column_name(i=x)
                if n:
                    names += n
        return names

    if isinstance(select, list):
        for i in select:
            result += extract_column_name(i)
    else:
        result += extract_column_name(select)
    return result


def find_first_node(node_key, parse_result):
    """
    Searches a parsed query for item with matching node_key.
    :param node_key: (str) - The key to find.
    :param parse_result (dict) - Parsed query
    :return: (dict) - Returns item as dictionary to preserve original key/value pair.
    """
    if node_key in parse_result:
        return parse_result[node_key]

    for k in parse_result:
        a = None

        if isinstance(parse_result, dict):
            if isinstance(parse_result[k], dict) or isinstance(parse_result[k], list):
                a = find_first_node(node_key, parse_result[k])
        elif isinstance(parse_result, list):
            a = find_first_node(node_key, k)

        if a is not None:
            return a

    return None


class Parser(object):
    parser = None
    known_types = known_types
    union_keywords = unions
    known_ops = KNOWN_OPS
    precedence = precedence
    join_keywords = join_keywords

    reserved = reserved
    durations = durations

    def __init__(self):
        engine = Engine().use()
        engine.add_ignore(Literal("--") + restOfLine)
        engine.add_ignore(Literal("#") + restOfLine)

        # IDENTIFIER
        literal_string = Regex(r'\"(\"\"|[^"])*\"').addParseAction(unquote)
        mysql_ident = Regex(r"\`(\`\`|[^`])*\`").addParseAction(unquote)
        sqlserver_ident = Regex(r"\[(\]\]|[^\]])*\]").addParseAction(unquote)
        placeholder_pattern = Regex(r"(\'[\w\d]*\{\S+\}[\w\d]*\')").addParseAction(unquote)
        ident = Combine(
            ~MatchFirst(self.reserved)
            + (delimitedList(
                Literal("*")
                | literal_string
                | placeholder_pattern
                | mysql_ident
                | sqlserver_ident
                | Word(IDENT_CHAR),
                separator=".",
                combine=True,
            )
            )
        ).set_parser_name("identifier")

        # EXPRESSIONS

        # CASE
        case = (
                CASE
                + Group(ZeroOrMore(
            (WHEN + expr("when") + THEN + expr("then")).addParseAction(to_when_call)
        ))("case")
                + Optional(ELSE + expr("else"))
                + END
        ).addParseAction(to_case_call)

        # SWITCH
        switch = (
                CASE
                + expr("value")
                + Group(ZeroOrMore(
            (WHEN + expr("when") + THEN + expr("then")).addParseAction(to_when_call)
        ))("case")
                + Optional(ELSE + expr("else"))
                + END
        ).addParseAction(to_switch_call)
        # CAST
        cast = Group(
            CAST("op") + LB + expr("params") + AS + self.known_types("params") + RB
        ).addParseAction(to_json_call)

        _standard_time_intervals = MatchFirst([
            Keyword(d, caseless=True).addParseAction(lambda t: self.durations[t[0].lower()])
            for d in self.durations.keys()
        ]).set_parser_name("duration")("params")

        duration = (realNum | intNum | placeholder_pattern)("params") + _standard_time_intervals

        interval = (
                INTERVAL + ("'" + delimitedList(duration) + "'" | duration)
        ).addParseAction(to_interval_call)

        timestamp = (
                time_functions("op")
                + (
                        sqlString("params")
                        | MatchFirst([
                    Keyword(t, caseless=True).addParseAction(lambda t: t.lower()) for t in times
                ])("params")
                )
        ).addParseAction(to_json_call)

        extract = (
                Keyword("extract", caseless=True)("op")
                + LB
                + (_standard_time_intervals | expr("params"))
                + FROM
                + expr("params")
                + RB
        ).addParseAction(to_json_call)

        namedColumn = Group(
            Group(expr)("value") + Optional(Optional(AS) + Group(ident))("name")
        )

        distinct = (
                DISTINCT("op") + delimitedList(namedColumn)("params")
        ).addParseAction(to_json_call)

        ordered_sql = Forward()

        call_function = (
                ident("op")
                + LB
                + Optional(Group(ordered_sql) | delimitedList(expr))("params")
                + Optional(
            Keyword("ignore", caseless=True) + Keyword("nulls", caseless=True)
        )("ignore_nulls")
                + RB
        ).addParseAction(to_json_call)

        compound = (
                NULL
                | TRUE
                | FALSE
                | NOCASE
                | interval
                | timestamp
                | extract
                | case
                | switch
                | cast
                | distinct
                | (LB + Group(ordered_sql) + RB)
                | (LB + Group(delimitedList(expr)).addParseAction(to_tuple_call) + RB)
                | sqlString.set_parser_name("string")
                | call_function
                | self.known_types
                | realNum.set_parser_name("float")
                | intNum.set_parser_name("int")
                | ident
        )

        expr << (
                (
                    infixNotation(
                        compound,
                        [
                            (
                                o,
                                1 if o in unary_ops else (3 if isinstance(o, tuple) else 2),
                                RIGHT_ASSOC if o in unary_ops else LEFT_ASSOC,
                                to_json_operator,
                            )
                            for o in self.known_ops
                        ],
                    ).set_parser_name("expression")
                )("value")
                + Optional(window)
        ).addParseAction(to_expression_call)

        alias = (
            (Group(ident) + Optional(LB + delimitedList(ident("col")) + RB))("name")
                .set_parser_name("alias")
                .addParseAction(to_alias)
        )

        selectColumn = (
            Group(
                Group(expr).set_parser_name("expression1")("value")
                + Optional(Optional(AS) + alias)
                | Literal("*")("value")
            )
                .set_parser_name("column")
                .addParseAction(to_select_call)
        )
        table_source = (
                ((LB + ordered_sql + RB) | call_function)("value").set_parser_name("table source")
                + Optional(Optional(AS) + alias)
                | (ident("value").set_parser_name("table name") + Optional(AS) + alias)
                | ident.set_parser_name("table name")
        )
        join = ((
                        CROSS_JOIN
                        | FULL_JOIN
                        | FULL_OUTER_JOIN
                        | INNER_JOIN
                        | JOIN
                        | LEFT_JOIN
                        | LEFT_OUTER_JOIN
                        | RIGHT_JOIN
                        | RIGHT_OUTER_JOIN
                )("op")
                + Group(table_source)("join")
                + Optional((ON + expr("on")) | (USING + expr("using")))
                ).addParseAction(to_join_call)
        unordered_sql = Group(
            SELECT
            + Optional(
                TOP
                + expr("value")
                + Optional(Keyword("percent", caseless=True))("percent")
                + Optional(WITH + Keyword("ties", caseless=True))("ties")
            )("top").addParseAction(to_top_clause)
            + delimitedList(selectColumn)("select")
            + Optional(
                (FROM + delimitedList(Group(table_source)) + ZeroOrMore(join))("from")
                + Optional(WHERE + expr("where"))
                + Optional(GROUP_BY + delimitedList(Group(namedColumn))("groupby"))
                + Optional(HAVING + expr("having"))
            )
        ).set_parser_name("unordered sql")
        ordered_sql << (
                (unordered_sql + ZeroOrMore((MatchFirst(self.union_keywords)) + unordered_sql))("union")
                + Optional(ORDER_BY + delimitedList(Group(sortColumn))("orderby"))
                + Optional(LIMIT + expr("limit"))
                + Optional(OFFSET + expr("offset"))
        ).set_parser_name("ordered sql").addParseAction(to_union_call)

        statement = Forward()
        statement << (
                Optional(
                    WITH + delimitedList(Group(ident("name") + AS + LB + statement("value") + RB))
                )("with")
                + Group(ordered_sql)("query")
        ).addParseAction(to_statement)
        self.parser = statement
        engine.release()

    def parse(self, sql):
        from moz_sql_parser.utils import scrub
        sql = sql.rstrip().rstrip(";")
        parse_result = self.parser.parseString(sql, parseAll=True)
        return scrub(parse_result)
