# Cycloidal's Disc Drawing
import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

def cos(angle):
    return math.cos(math.radians(angle))

def sin(angle):
    return math.sin(math.radians(angle))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
    # You Can Put the Dimention of Your Cyloidal Drive in Here.
    # Noted: You can change the number come after "=".
###############################################################################################################################################################################################
        pin_radius = 0.25                # The radius of your each pin for your Cycloidal Drive (Unit: Centimeters).
        pin_circle_radius = 5            # The radius of the circle of your all pins for Cycloidal Drive and it also can consider as the full size of your cycloidal Drive (Unit: Centimeters).
        number_of_pins = 10              # The number of your pins to put for your Cycloidal Drive (Unit: None)
        contraction = 0.2                # Contraction=Eccentricities that your put for input shaft of your Cycloidal Drive. (Unit: Centimeters)
###############################################################################################################################################################################################
    # End here ( You don't need to change anything from here because the below codes are the equation that we put for fusion to draw the shape for your cycloidal Drive's Disc ).
    # Noted: After your done putting your dimention, don't forget to save this codes file (Ctrl+S).

        rolling_circle_radius = pin_circle_radius / number_of_pins 
        reduction_ratio = number_of_pins - 1 
        cycloid_base_radius = reduction_ratio * rolling_circle_radius 
        last_point=None
        line=None
        lines=[]

        for angle in drange(0,360/reduction_ratio,0.5):
            x =  (cycloid_base_radius + rolling_circle_radius) * cos(angle)
            y =  (cycloid_base_radius + rolling_circle_radius) * sin(angle)
            point_x = x + (rolling_circle_radius - contraction) * cos(number_of_pins*angle)
            point_y = y + (rolling_circle_radius - contraction) * sin(number_of_pins*angle)
           
            if angle==0:              
                last_point = adsk.core.Point3D.create(point_x,point_y, 0)
                
            else:
                line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                    last_point, 
                    adsk.core.Point3D.create(point_x,point_y, 0)
                    )
                last_point=line.endSketchPoint
                lines.append(line)

            app.activeViewport.refresh()

        curves = sketch.findConnectedCurves(lines[0])
        dirPoint = adsk.core.Point3D.create(0, 0, 0)
        offsetCurves = sketch.offset(curves, dirPoint, pin_radius)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# END