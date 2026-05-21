
package aiopscare.authz

default allow := false

allow if {
    input.path == "/"
}

allow if {
    input.path == "/docs"
}

allow if {
    input.path == "/openapi.json"
}

allow if {
    input.path == "/metrics"
}

allow if {
    input.path == "/predict"
}
