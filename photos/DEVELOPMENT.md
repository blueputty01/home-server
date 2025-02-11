# Interpolation syntax

Interpolation is applied for unquoted and double-quoted values. Both braced (${VAR}) and unbraced ($VAR) expressions are supported.

For braced expressions, the following formats are supported:

Direct substitution
${VAR} -> value of VAR
Default value
${VAR:-default} -> value of VAR if set and non-empty, otherwise default
${VAR-default} -> value of VAR if set, otherwise default
Required value
${VAR:?error} -> value of VAR if set and non-empty, otherwise exit with error
${VAR?error} -> value of VAR if set, otherwise exit with error
Alternative value
${VAR:+replacement} -> replacement if VAR is set and non-empty, otherwise empty
${VAR+replacement} -> replacement if VAR is set, otherwise empty
For more information, see Interpolation in the Compose Specification.

# Ways to set variables with interpolation

Docker Compose can interpolate variables into your Compose file from multiple sources.

Note that when the same variable is declared by multiple sources, precedence applies:

1. Variables from your shell environment
2. If --env-file is not set, variables set by an .env file in local working directory (PWD)
3. Variables from a file set by --env-file or an .env file in project directory

You can check variables and values used by Compose to interpolate the Compose model by running docker compose config --environment.
