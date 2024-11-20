# SPARQL triplet store

## oxigraph
The developer of oxigraph have had the brilliant idea of saving the importnat info about
docker, endpoints etc inside the cli/README.md file. Here is the link:
https://github.com/oxigraph/oxigraph/blob/main/cli/README.md

- port: 7878
- endpoint (query): /query (see [documentation](https://www.w3.org/TR/sparql11-protocol/#query-operation))
- endpoint (update): /update (see [documentation](https://www.w3.org/TR/sparql11-update/))
- endpoint (store): /store (see [documentation?](https://www.w3.org/TR/2013/REC-sparql11-http-rdf-update-20130321/))
- To load data in bulk from files there is a command `oxigraph load ...`

## List of Actively maintained SPARQL Databases

<table>
    <tr>
        <th></th>
        <th>Language</th>
        <th>docker</th>
        <th>link</th>
        <th>notes</th>
    </tr>
    <tr>
        <td>RDF4J</td>
        <td>Java</td>
        <td></td>
        <td>https://rdf4j.org/download/</td>
    </tr>
    <tr>
        <td>Apache Jena</td>
        <td>Java</td>
        <td></td>
        <td>https://jena.apache.org/</td>
    </tr>
    <tr>
        <td>Corese</td>
        <td>Java (Maven)</td>
        <td></td>
        <td>https://github.com/Wimmics/corese</td>
    </tr>
    <tr>
        <td>ontop</td>
        <td>Java (Maven)</td>
        <td>✓</td>
        <td>https://github.com/ontop/ontop</td>
        <td>Wrapper for a SQL DB</td>
    </tr>
    <tr>
        <td>oxygraph</td>
        <td>RUST</td>
        <td>✓</td>
        <td>
            https://github.com/oxigraph/oxigraph/tree/main/cli
        </td>
        <td>Heavy development, based on RockDB key-value database</td>
    </tr>
    <tr>
        <td>QLever</td>    
        <td>C++</td>
        <td>✓</td>
        <td>https://github.com/ad-freiburg/qlever</td>
        <td>Fast on large Knowledge Graphs</td>
    </tr>
    <tr>
        <td>Virtuoso</td>
        <td>C/C++/...</td>
        <td>✓</td>
        <td>https://github.com/openlink/virtuoso-opensource</td>
    </tr>
</table>

