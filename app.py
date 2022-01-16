#!/usr/bin/env python3

import aws_cdk as cdk

from thirukkuralpoem.thirukkuralpoem_stack import ThirukkuralpoemStack


app = cdk.App()
ThirukkuralpoemStack(app, "thirukkuralpoem")

app.synth()
