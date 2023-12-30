# 13. Set of segments on a straight line

Implemented commands:

1. `CREATE set_name;`

2. `INSERT set_name [l,h];`

3. `PRINT_TREE set_name;`

4. `CONTAINS set_name [l,h];`

5. `SEARCH set_name *[WHERE query];`

```
query := CONTAINED_BY [l,h];
       | INTERSECTS [l,h];
       | RIGHT_OF x;
```

```
set_name :=  [a-zA-Z][a-zA-Z0-9_]*
```

```
[l,h] : l <= h
```

In the CLI:

- Empty lines are ignored

- Lines not ending with `;` will bring up a continuation prompt

- everything after a `;` is ignored (on the lexer / cli level)

### Possible improvements:

1. Responsibilitiy distribution between lexer and parser could be improved (currently *lexer interpretes* too much information about the input)
2. ... and many other
