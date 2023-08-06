// t100_flatland_node_subsystem.mss
diagram class
notation Starr
presentation default
orientation landscape
sheet D
padding 50 250 50 20 // left, bottom, top, right diagram padding between canvas margin to avoid frame overlap
frame OS Engineer
frame_presentation default
nodes
    Annotation Layout 3,3
    Block 1,3
    Canvas 4,1
    Cell 4,8 >right
    Column 3,7
    Compartment 5-6,15-16
    Compartment Type 8-9,14
    Data Compartment 4,16 >top
    Diagram 4,3
    Diagram Notation 10,6
    Diagram Type 8-9,8
    Field Spec 1,5
    Grid 4,5
    Layout Specification 9,1
    Node 5,12
    Node Type 8-9,12
    Non Spanning Node 6,10
    Notation 11,8
    Row 5,7
    Sheet 1,1
    Spanning Node 4,10
    Text Line 5-6,18
    Title Compartment 4,15 >top
connectors
    +R1 : -/1 l|Row : +/1 t|Grid
    +R2 : -/1 l|Column : +/1 b|Grid
    -R3 : +/1 b|Row : +/1 t*|Column, l|Cell
    +R4 : +/3 r|Node Type : -/3 l*|Compartment Type
    +R5 : +/1 b|Node Type : +/1 t*|Node
    -R6.2 : +/1 b|Compartment Type : +/2 r|Node, l|Compartment
    +R7 : -/1 r|Compartment : -/1 l*|Text Line
    -R8 : b|Compartment { t|Title Compartment, t|Data Compartment }
    +R9 : -/2 t+1|Compartment Type : -/2 r+1|Compartment Type : L10R-2 L15R-2
    -R10 : -/2 r|Diagram : +/2 l*|Grid
    +R11.2 : +/1 t+2|Diagram : +/1 l|Diagram Type
    +R12.2 : -/1 t|Cell : -/2 t-1|Node : L7
    +R13 : -/2 b|Canvas : -/2 t*|Sheet
    -R14 : -/2 r|Canvas : +/2 l*|Diagram
    +R15 : -/1 r|Diagram Type : -/1 l*|Node Type
    +R16.1 : -/2 l+1|Annotation Layout : +/2 b+1|Canvas
    +R17 : -/1 t*|Block : -/1 b|Annotation Layout
    +R18 : -/1 r|Block : -/1 l*|Field Spec
    +R20 : l|Node { r|Non Spanning Node, r|Spanning Node }
    +R22 : +/2 r+1|Row : +/2 t|Spanning Node
    -R23 : -/2 r-1|Row : -/2 t-2|Spanning Node
    +R24 : +/1 r+1|Column : -/2 b-1|Spanning Node
    -R25 : -/1 r-1|Column : +/2 b+1|Spanning Node
    +R30.2 : -/1 t-2|Diagram : -/1 l|Diagram Notation
    +R32 : +/1 b|Notation : +/1 t*|Diagram Type, r|Diagram Notation

