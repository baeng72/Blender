import bpy
from mathutils import Vector
import math
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
                       
                       

        
                     
def getMaterial(mat_name):
    print('getMaterial(',mat_name,')')
    mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))
    return mat         

def getShader(mat):
    #print('getShader(',mat.name,')')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    shader = nodes.get('Principled BSDF') or nodes.new('ShaderNodeBsdfPrincipled')
    return shader          

def getBump(mat):
    print('getBump(',mat.name,')')
    nodes = mat.node_tree.nodes
    bump = nodes.get('Bump') or nodes.new('ShaderNodeBump')
    return bump  


def getVoronoi(mat):
    print('getVoronoi(',mat.name,')')
    nodes = mat.node_tree.nodes
    voronoi = nodes.get('Voronoi') or nodes.new('ShaderNodeTexVoronoi')
    return voronoi  

def getNode(mat,name,type):
    #print('getNode(',mat.name,',',name,',',type,')')
    nodes = mat.node_tree.nodes
    node = nodes.get(name) or nodes.new(type)
    node.name=name
    node.label=name
    return node


def setShaderColor(shader,basecol):
    shader.inputs['Base Color'].default_value = [0.5,0.5,0.5,1]
    if basecol=='GOLD':
            shader.inputs['Base Color'].default_value = [0.83,0.69,0.22,1]  
    elif basecol=='SILVER':          
            shader.inputs['Base Color'].default_value = [0.75,0.75,0.75,1]  
    elif basecol=='BRONZE':          
            shader.inputs['Base Color'].default_value = [0.8,0.5,0.2,1]     
    elif basecol=='COPPER':          
            shader.inputs['Base Color'].default_value = [0.72,0.45,0.2,1]   
    elif basecol=='ALUMINIUM':          
            shader.inputs['Base Color'].default_value = [0.54,0.56,0.58,1]   
    elif basecol=='IRON':
            shader.inputs['Base Color'].default_value = [0.79,0.8,0.8,1]   
    elif basecol=='CHROMIUM':
            shader.inputs['Base Color'].default_value = [0.77,0.78,0.78,1]                       
    elif basecol=='NICKEL':
            shader.inputs['Base Color'].default_value = [0.709,0.713,0.709,1]                       
    elif basecol=='TITANIUM':
            shader.inputs['Base Color'].default_value = [0.529,0.486,0.505,1]                       
    elif basecol=='COBALT':
            shader.inputs['Base Color'].default_value = [0,0.28,0.57,1]                       

def printGroupTree(group):
    print('printNodeTree('+group.name+')')
    nodes = group.nodes
    for i in range(len(nodes)):
        print(nodes[i].name + ': ' +nodes[i].bl_idname + ' '+nodes[i].bl_label)
        
def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))        

def getGrimeGroup():
    print('getGrimeGroup()')
    grimeGroup = bpy.data.node_groups.get('Grime') or bpy.data.node_groups.new('Grime','ShaderNodeTree')
    grimeGroupInputs = grimeGroup.nodes.get('GrimeGroupInputs') or grimeGroup.nodes.new('NodeGroupInput')
    grimeGroupInputs.name = 'GrimeGroupInputs'
    grimeGroupOutputs = grimeGroup.nodes.get('GrimeGroupOutputs') or grimeGroup.nodes.new('NodeGroupOutput')
    grimeGroupOutputs.name= 'GrimeGroupOutputs'
    grimeInputs = grimeGroup.inputs
    vectorInput = grimeInputs.get('Vector') or grimeInputs.new('NodeSocketVector','Vector')
    baseColorInput = grimeInputs.get('Base Color') or grimeInputs.new('NodeSocketColor','Base Color')
    grimeColorInput = grimeInputs.get('Grime Color') or grimeInputs.new('NodeSocketColor','Grime Color')
    grimeStrengthInput = grimeInputs.get('Grime Strength') or grimeInputs.new('NodeSocketFloat','Grime Strength')
    grimeOutputs = grimeGroup.outputs
    baseColorOutput = grimeOutputs.get('Base Color') or grimeOutputs.new('NodeSocketColor','Base Color')


    nodes = grimeGroup.nodes
    links=grimeGroup.links
    waveTex1 = nodes.get('WaveTexture1') or nodes.new('ShaderNodeTexWave')
    waveTex1.name = 'WaveTexture1'
    waveTex1.inputs['Scale'].default_value=1
    waveTex1.inputs['Distortion'].default_value=150
    waveTex1.inputs['Detail'].default_value=15
    links.new(grimeGroupInputs.outputs['Vector'],waveTex1.inputs['Vector'])
    waveTex1.location = grimeGroupInputs.location + Vector((300,300))
    voronoi1 = nodes.get('Voronoi1') or nodes.new('ShaderNodeTexVoronoi')

    voronoi1.inputs['Scale'].default_value=4
    voronoi1.feature = 'DISTANCE_TO_EDGE'
    voronoi1.name = 'Voronoi1'
    links.new(waveTex1.outputs['Color'],voronoi1.inputs['Vector'])
    voronoi1.location = waveTex1.location + Vector((300,0))
    musgrave1 = nodes.get('MusgraveTexture1') or nodes.new('ShaderNodeTexMusgrave')
    musgrave1.name = 'MusgraveTexture1'
    musgrave1.inputs['Scale'].default_value=1
    musgrave1.inputs['Detail'].default_value=3
    musgrave1.inputs['Dimension'].default_value=0
    musgrave1.inputs['Lacunarity'].default_value=15
    links.new(grimeGroupInputs.outputs['Vector'],musgrave1.inputs['Vector'])
    musgrave1.location = grimeGroupInputs.location + Vector((300,0))
    musgrave2 = nodes.get('MusgraveTexture2') or nodes.new('ShaderNodeTexMusgrave')
    musgrave2.name = 'MusgraveTexture2'
    musgrave2.inputs['Scale'].default_value=25
    musgrave2.inputs['Detail'].default_value=3
    musgrave2.inputs['Dimension'].default_value=0
    musgrave2.inputs['Lacunarity'].default_value=15
    links.new(grimeGroupInputs.outputs['Vector'],musgrave2.inputs['Vector'])
    musgrave2.location = grimeGroupInputs.location + Vector((300,-300))
    voronoi2 = nodes.get('Voronoi2') or nodes.new('ShaderNodeTexVoronoi')
    voronoi2.inputs['Scale'].default_value=4
    voronoi2.feature = 'DISTANCE_TO_EDGE'
    voronoi2.name = 'Voronoi2'
    links.new(grimeGroupInputs.outputs['Vector'],voronoi2.inputs['Vector'])
    voronoi2.location = grimeGroupInputs.location + Vector((300,-600))
    waveTex2 = nodes.get('WaveTexture2') or nodes.new('ShaderNodeTexWave')
    waveTex2.name = 'WaveTexture2'
    waveTex2.inputs['Distortion'].default_value=0
    waveTex2.inputs['Detail'].default_value=2
    links.new(voronoi2.outputs['Distance'],waveTex2.inputs['Scale'])
    waveTex2.location = voronoi2.location + Vector((300,0))
    lighten1 = nodes.get('Lighten1') or nodes.new('ShaderNodeMixRGB')
    lighten1.name='Lighten1'
    lighten1.blend_type='LIGHTEN'
    lighten1.inputs['Fac'].default_value=1
    links.new(voronoi1.outputs['Distance'],lighten1.inputs['Color1'])
    links.new(musgrave1.outputs['Fac'],lighten1.inputs['Color2'])
    lighten1.location = voronoi1.location+ Vector((300,-150))
    lighten2 = nodes.get('Lighten2') or nodes.new('ShaderNodeMixRGB')
    lighten2.name = 'Lighten2'
    lighten2.blend_type='LIGHTEN'
    lighten2.inputs['Fac'].default_value=1
    links.new(lighten1.outputs['Color'],lighten2.inputs['Color1'])
    links.new(musgrave2.outputs['Fac'],lighten2.inputs['Color2'])
    lighten2.location = lighten1.location + Vector((300,0))
    overlay = nodes.get('Overlay') or nodes.new('ShaderNodeMixRGB')
    overlay.name='Overlay'
    overlay.blend_type='OVERLAY'
    overlay.inputs['Fac'].default_value=0.3
    links.new(lighten2.outputs['Color'],overlay.inputs['Color1'])
    links.new(waveTex2.outputs['Color'],overlay.inputs['Color2'])
    overlay.location = lighten2.location + Vector((300,0))
    geometry = nodes.get('Geometry') or nodes.new('ShaderNodeNewGeometry')
    geometry.name = 'Geometry'
    geometry.location = lighten2.location + Vector((0,300))
    colorramp = nodes.get('Colorramp') or nodes.new('ShaderNodeValToRGB')    
    colorramp.name = 'Colorramp'
    colorramp.color_ramp.elements[0].color=[1,1,1,1]
    colorramp.color_ramp.elements[0].position = 0.418
    colorramp.color_ramp.elements[1].color=[0,0,0,1]
    colorramp.color_ramp.elements[1].position=0.555
    links.new(geometry.outputs['Pointiness'],colorramp.inputs['Fac'])
    colorramp.location = geometry.location+Vector((300,0))
    multiply = nodes.get('Multiply') or nodes.new('ShaderNodeMixRGB')
    multiply.name ='Multiply'
    multiply.blend_type='MULTIPLY'
    multiply.inputs['Fac'].default_value=1
    
    links.new(colorramp.outputs['Color'],multiply.inputs['Color1'])
    links.new(overlay.outputs['Color'],multiply.inputs['Color2'])
    multiply.location = colorramp.location+Vector((300,0))
    #colorramp2 = nodes.get('Colorramp2') or nodes.new('ShaderNodeValToRGB')
    #colorramp2.name = 'Colorramp2'
    #colorramp2.color_ramp.elements[1].position=grimeStrengthInput.default_value
    #links.new(multiply.outputs['Color'],colorramp2.inputs['Fac'])
    #colorramp2.location = multiply.location + Vector((300,0))
    mapRange = nodes.get('MapRange') or nodes.new('ShaderNodeMapRange')
    mapRange.name = 'MapRange'
    links.new(multiply.outputs['Color'],mapRange.inputs['Value'])
    mapRange.location = multiply.location + Vector((300,0))
    multiply2 = nodes.get('Multiply2') or nodes.new('ShaderNodeMixRGB')
    multiply2.name='Multiply2'
    multiply2.blend_type='MULTIPLY'
    #multiply2.location = colorramp2.location + Vector((300,0))
    multiply2.location = mapRange.location + Vector((300,0))
    #links.new(colorramp2.outputs['Color'],multiply2.inputs['Fac'])
    links.new(mapRange.outputs['Result'],multiply2.inputs['Fac'])
    links.new(grimeGroupInputs.outputs['Base Color'],multiply2.inputs['Color1'])
    links.new(grimeGroupInputs.outputs['Grime Color'],multiply2.inputs['Color2'])
    links.new(grimeGroupInputs.outputs['Grime Strength'],mapRange.inputs['From Max'])
    links.new(multiply2.outputs['Color'],grimeGroupOutputs.inputs['Base Color'])
    grimeGroupOutputs.location = multiply2.location + Vector((300,0))
    
    #printGroupTree(grimeGroup)
    return grimeGroup

def getScratchesGroup():
    print('getScratchesGroup()')
    
    scratchGroup = bpy.data.node_groups.get('Scratch') or bpy.data.node_groups.new('Scratch','ShaderNodeTree')
    scratchGroupInputs = scratchGroup.nodes.get('ScratchGroupInputs') or scratchGroup.nodes.new('NodeGroupInput')
    scratchGroupInputs.name = 'ScratchGroupInputs'
    scratchGroupOutputs = scratchGroup.nodes.get('ScratchGroupOutputs') or scratchGroup.nodes.new('NodeGroupOutput')
    scratchGroupOutputs.name= 'ScratchGroupOutputs'
    scratchInputs = scratchGroup.inputs
    vectorInput = scratchInputs.get('Vector') or scratchInputs.new('NodeSocketVector','Vector')
    baseColorInput = scratchInputs.get('Base Color') or scratchInputs.new('NodeSocketColor','Base Color')
    scratchColorInput = scratchInputs.get('Scratch Color') or scratchInputs.new('NodeSocketColor','Scratch Color')
    #scratchStrengthInput = scratchInputs.get('scratch Strength') or scratchInputs.new('NodeSocketFloat','Scratch Strength')
    scratchOutputs = scratchGroup.outputs
    baseColorOutput = scratchOutputs.get('Base Color') or scratchOutputs.new('NodeSocketColor','Base Color')
    nodes = scratchGroup.nodes
    links= scratchGroup.links
    noiseTex1 = nodes.get('NoiseTexture1') or nodes.new('ShaderNodeTexNoise')
    noiseTex1.name = 'NoiseTexture1'
    noiseTex1.inputs['Scale'].default_value=15
    noiseTex1.inputs['Detail'].default_value=2
    noiseTex1.inputs['Distortion'].default_value=0
    links.new(scratchGroupInputs.outputs['Vector'],noiseTex1.inputs['Vector'])
    noiseTex1.location = scratchGroupInputs.location + Vector((600,1200))
    brightContrast1 = nodes.get('BrigthContrast1') or nodes.new('ShaderNodeBrightContrast')
    brightContrast1.name = 'BrigthContrast1'
    brightContrast1.inputs['Bright'].default_value=1
    brightContrast1.inputs['Contrast'].default_value=10
    links.new(noiseTex1.outputs['Fac'],brightContrast1.inputs['Color'])
    brightContrast1.location = noiseTex1.location + Vector((300,00))

    waveTex1 = nodes.get('WaveTexture1') or nodes.new('ShaderNodeTexWave')
    waveTex1.name = 'WaveTexture1'
    waveTex1.inputs['Scale'].default_value=25
    waveTex1.inputs['Distortion'].default_value=2
    waveTex1.inputs['Detail'].default_value=2    
    links.new(scratchGroupInputs.outputs['Vector'],waveTex1.inputs['Vector'])
    waveTex1.location = scratchGroupInputs.location + Vector((600,900))
    brightContrast2 = nodes.get('BrigthContrast2') or nodes.new('ShaderNodeBrightContrast')
    brightContrast2.name = 'BrigthContrast2'
    brightContrast2.inputs['Bright'].default_value=1
    brightContrast2.inputs['Contrast'].default_value=2
    links.new(waveTex1.outputs['Color'],brightContrast2.inputs['Color'])
    brightContrast2.location = waveTex1.location + Vector((300,0))
    add1 = nodes.get('Add1') or nodes.new('ShaderNodeMixRGB')
    add1.name = 'Add1'
    add1.blend_type='ADD'
    add1.inputs['Fac'].default_value=1
    links.new(brightContrast1.outputs['Color'],add1.inputs['Color1'])
    links.new(brightContrast2.outputs['Color'],add1.inputs['Color2'])
    add1.location = brightContrast1.location + Vector((300,-150))
    mapping1 = nodes.get('Mapping1') or nodes.new('ShaderNodeMapping')
    mapping1.name = 'Mapping1'
    mapping1.inputs['Rotation'].default_value[0] = math.radians(90)
    links.new(scratchGroupInputs.outputs['Vector'],mapping1.inputs['Vector'])
    mapping1.location = scratchGroupInputs.location + Vector((450,600))
    noiseTex2 = nodes.get('NoiseTexture2') or nodes.new('ShaderNodeTexNoise')
    noiseTex2.name = 'NoiseTexture2'
    noiseTex2.inputs['Scale'].default_value=15
    noiseTex2.inputs['Detail'].default_value=2
    noiseTex2.inputs['Distortion'].default_value=0
    links.new(mapping1.outputs['Vector'],noiseTex2.inputs['Vector'])
    noiseTex2.location = mapping1.location + Vector((200,0))
    brightContrast3 = nodes.get('BrigthContrast3') or nodes.new('ShaderNodeBrightContrast')
    brightContrast3.name = 'BrigthContrast3'
    brightContrast3.inputs['Bright'].default_value=1
    brightContrast3.inputs['Contrast'].default_value=10
    links.new(noiseTex2.outputs['Fac'],brightContrast3.inputs['Color'])
    brightContrast3.location = noiseTex2.location + Vector((300,00))
    waveTex2 = nodes.get('WaveTexture2') or nodes.new('ShaderNodeTexWave')
    waveTex2.name = 'WaveTexture2'
    waveTex2.inputs['Scale'].default_value=25
    waveTex2.inputs['Distortion'].default_value=2
    waveTex2.inputs['Detail'].default_value=2    
    links.new(mapping1.outputs['Vector'],waveTex2.inputs['Vector'])
    waveTex2.location = mapping1.location + Vector((200,-200))
    brightContrast4 = nodes.get('BrigthContrast4') or nodes.new('ShaderNodeBrightContrast')
    brightContrast4.name = 'BrigthContrast4'
    brightContrast4.inputs['Bright'].default_value=1
    brightContrast4.inputs['Contrast'].default_value=2
    links.new(waveTex2.outputs['Color'],brightContrast4.inputs['Color'])
    brightContrast4.location = waveTex2.location + Vector((300,0))
    add2 = nodes.get('Add2') or nodes.new('ShaderNodeMixRGB')
    add2.name = 'Add2'
    add2.blend_type='ADD'
    add2.inputs['Fac'].default_value=1
    links.new(brightContrast3.outputs['Color'],add2.inputs['Color1'])
    links.new(brightContrast4.outputs['Color'],add2.inputs['Color2'])
    add2.location = brightContrast3.location + Vector((250,-150))
    multiply1 = nodes.get('Multiply1') or nodes.new('ShaderNodeMixRGB')
    multiply1.name = 'Multiply1'
    multiply1.blend_type='MULTIPLY'
    links.new(add1.outputs['Color'],multiply1.inputs['Color1'])
    links.new(add2.outputs['Color'],multiply1.inputs['Color2'])
    multiply1.location = add1.location + Vector((300,-150))
    mapping2 = nodes.get('Mapping2') or nodes.new('ShaderNodeMapping')
    mapping2.name = 'Mapping2'
    mapping2.inputs['Rotation'].default_value[1] = math.radians(45)
    links.new(scratchGroupInputs.outputs['Vector'],mapping2.inputs['Vector'])
    mapping2.location = scratchGroupInputs.location + Vector((450,150))
    noiseTex3 = nodes.get('NoiseTexture3') or nodes.new('ShaderNodeTexNoise')
    noiseTex3.name = 'NoiseTexture3'
    noiseTex3.inputs['Scale'].default_value=25
    noiseTex3.inputs['Detail'].default_value=2
    noiseTex3.inputs['Distortion'].default_value=0
    links.new(mapping2.outputs['Vector'],noiseTex3.inputs['Vector'])
    noiseTex3.location = mapping2.location + Vector((200,0))
    brightContrast4 = nodes.get('BrigthContrast4') or nodes.new('ShaderNodeBrightContrast')
    brightContrast4.name = 'BrigthContrast4'
    brightContrast4.inputs['Bright'].default_value=1
    brightContrast4.inputs['Contrast'].default_value=10
    links.new(noiseTex3.outputs['Fac'],brightContrast4.inputs['Color'])
    brightContrast4.location = noiseTex3.location + Vector((300,00))
    waveTex3 = nodes.get('WaveTexture3') or nodes.new('ShaderNodeTexWave')
    waveTex3.name = 'WaveTexture3'
    waveTex3.inputs['Scale'].default_value=50
    waveTex3.inputs['Distortion'].default_value=0
    waveTex3.inputs['Detail'].default_value=2    
    links.new(mapping2.outputs['Vector'],waveTex3.inputs['Vector'])
    waveTex3.location = mapping2.location + Vector((200,-200))
    brightContrast5 = nodes.get('BrigthContrast5') or nodes.new('ShaderNodeBrightContrast')
    brightContrast5.name = 'BrigthContrast5'
    brightContrast5.inputs['Bright'].default_value=1
    brightContrast5.inputs['Contrast'].default_value=2
    links.new(waveTex3.outputs['Color'],brightContrast5.inputs['Color'])
    brightContrast5.location = waveTex3.location + Vector((300,0))
    add3 = nodes.get('Add3') or nodes.new('ShaderNodeMixRGB')
    add3.name = 'Add3'
    add3.blend_type='ADD'
    add3.inputs['Fac'].default_value=1
    links.new(brightContrast4.outputs['Color'],add3.inputs['Color1'])
    links.new(brightContrast5.outputs['Color'],add3.inputs['Color2'])
    add3.location = brightContrast4.location + Vector((250,-50))
    mapping3 = nodes.get('Mapping3') or nodes.new('ShaderNodeMapping')
    mapping3.name = 'Mapping3'
    mapping3.inputs['Rotation'].default_value[2] = math.radians(45)
    links.new(scratchGroupInputs.outputs['Vector'],mapping3.inputs['Vector'])
    mapping3.location = scratchGroupInputs.location + Vector((450,-300))
    noiseTex4 = nodes.get('NoiseTexture4') or nodes.new('ShaderNodeTexNoise')
    noiseTex4.name = 'NoiseTexture4'
    noiseTex4.inputs['Scale'].default_value=25
    noiseTex4.inputs['Detail'].default_value=2
    noiseTex4.inputs['Distortion'].default_value=0
    links.new(mapping3.outputs['Vector'],noiseTex4.inputs['Vector'])
    noiseTex4.location = mapping3.location + Vector((200,0))
    brightContrast6 = nodes.get('BrigthContrast6') or nodes.new('ShaderNodeBrightContrast')
    brightContrast6.name = 'BrigthContrast6'
    brightContrast6.inputs['Bright'].default_value=1
    brightContrast6.inputs['Contrast'].default_value=10
    links.new(noiseTex4.outputs['Fac'],brightContrast6.inputs['Color'])
    brightContrast6.location = noiseTex4.location + Vector((300,00))
    waveTex4 = nodes.get('WaveTexture4') or nodes.new('ShaderNodeTexWave')
    waveTex4.name = 'WaveTexture4'
    waveTex4.inputs['Scale'].default_value=50
    waveTex4.inputs['Distortion'].default_value=0
    waveTex4.inputs['Detail'].default_value=2    
    links.new(mapping3.outputs['Vector'],waveTex4.inputs['Vector'])
    waveTex4.location = mapping3.location + Vector((200,-300))
    brightContrast7 = nodes.get('BrigthContrast7') or nodes.new('ShaderNodeBrightContrast')
    brightContrast7.name = 'BrigthContrast7'
    brightContrast7.inputs['Bright'].default_value=1
    brightContrast7.inputs['Contrast'].default_value=2
    links.new(waveTex4.outputs['Color'],brightContrast7.inputs['Color'])
    brightContrast7.location = waveTex4.location + Vector((300,0))
    add4 = nodes.get('Add4') or nodes.new('ShaderNodeMixRGB')
    add4.name = 'Add4'
    add4.blend_type='ADD'
    add4.inputs['Fac'].default_value=1
    links.new(brightContrast6.outputs['Color'],add4.inputs['Color1'])
    links.new(brightContrast7.outputs['Color'],add4.inputs['Color2'])
    add4.location = brightContrast6.location + Vector((250,-150))
    multiply2 = nodes.get('Multiply2') or nodes.new('ShaderNodeMixRGB')
    multiply2.name = 'Multiply2'
    multiply2.blend_type='MULTIPLY'
    links.new(add3.outputs['Color'],multiply2.inputs['Color1'])
    links.new(add4.outputs['Color'],multiply2.inputs['Color2'])
    multiply2.location = add3.location + Vector((300,-150))
    multiply3 = nodes.get('Multiply3') or nodes.new('ShaderNodeMixRGB')
    multiply3.name = 'Multiply3'
    multiply3.blend_type='MULTIPLY'
    multiply3.inputs['Fac'].default_value=1
    links.new(multiply1.outputs['Color'],multiply3.inputs['Color1'])
    links.new(multiply2.outputs['Color'],multiply3.inputs['Color2'])
    multiply3.location = multiply1.location + Vector((300,-300))
    multiply3.inputs['Fac'].default_value=1
    invert = nodes.get('Invert') or nodes.new('ShaderNodeInvert')
    invert.name = 'Invert'
    links.new(multiply3.outputs['Color'],invert.inputs['Color'])
    invert.location = multiply3.location+ Vector((300,0))
    geometry = nodes.get('Geometry') or nodes.new('ShaderNodeNewGeometry')
    geometry.name = 'Geometry'
    geometry.location = multiply1.location + Vector((0,300))
    colorramp = nodes.get('Colorramp') or nodes.new('ShaderNodeValToRGB')    
    colorramp.name = 'Colorramp'
    colorramp.color_ramp.elements[0].color=[0,0,0,0]
    colorramp.color_ramp.elements[0].position = 0.568
    colorramp.color_ramp.elements[1].color=[1,1,1,1]
    colorramp.color_ramp.elements[1].position=0.682
    links.new(geometry.outputs['Pointiness'],colorramp.inputs['Fac'])
    colorramp.location = geometry.location+Vector((300,0))
    multiply4 = nodes.get('Multiply4') or nodes.new('ShaderNodeMixRGB')
    multiply4.name ='Multiply4'
    multiply4.blend_type='MULTIPLY'
    multiply4.inputs['Fac'].default_value=1
    links.new(colorramp.outputs['Color'],multiply4.inputs['Color1'])
    links.new(invert.outputs['Color'],multiply4.inputs['Color2'])
    multiply4.location = colorramp.location + Vector((600,-150))
    colorramp2 = nodes.get('Colorramp') or nodes.new('ShaderNodeValToRGB')    
    colorramp2.name = 'Colorramp'
    colorramp2.color_ramp.elements[0].color=[0,0,0,0]
    colorramp2.color_ramp.elements[0].position = 0
    colorramp2.color_ramp.elements[1].color=[1,1,1,1]
    colorramp2.color_ramp.elements[1].position=0.327
    links.new(multiply4.outputs['Color'],colorramp2.inputs['Fac'])
    colorramp2.location = multiply4.location+Vector((300,-150))
    mix = nodes.get('Mix') or nodes.new('ShaderNodeMixRGB')
    mix.name='Mix'
    mix.blend_type='MIX'
    links.new(colorramp2.outputs['Color'],mix.inputs['Fac'])
    links.new(scratchGroupInputs.outputs['Base Color'],mix.inputs['Color1'])
    links.new(scratchGroupInputs.outputs['Scratch Color'],mix.inputs['Color2'])
#    links.new(grimeGroupInputs.outputs['Grime Strength'],mapRange.inputs['From Max'])
    links.new(mix.outputs['Color'],scratchGroupOutputs.inputs['Base Color'])
    scratchGroupOutputs.location = mix.location + Vector((300,-150))
    
    return scratchGroup

def getDustGroup():
    print('getDustGroup()')

    dustGroup = bpy.data.node_groups.get('Dust') or bpy.data.node_groups.new('Dust','ShaderNodeTree')
    dustInputs = dustGroup.inputs
    vectorInput = dustInputs.get('Vector') or dustInputs.new('NodeSocketVector','Vector')
    baseColorInput = dustInputs.get('Base Color') or dustInputs.new('NodeSocketFloat','Base Color')
    dustColorInput = dustInputs.get('Dust Color') or dustInputs.new('NodeSocketFloat','Dust Color')
    dustOutputs = dustGroup.outputs
    baseColorOutput = dustOutputs.get('Dust Color') or dustOutputs.new('NodeSocketFloat','Dust Color')
    printGroupTree(dustGroup)
    return dustGroup    

def printNodeTree(mat):
    print('printNodeTree('+mat.name+')')
    nodes = mat.node_tree.nodes
    for i in range(len(nodes)):
        print(nodes[i].name + ': ' +nodes[i].bl_idname)
        
def createLeather(mesh,matprops):#name,grime,scratches,dust,grimecolor):
    name = matprops.MatBaseType

    grime = matprops.Grime
    grimecolor = matprops.GrimeColor
    grimestrength = matprops.GrimeStrength
    plasticsmoothness = matprops.PlasticSmoothness
    scratches=matprops.Scratches
    scratchcolor = matprops.ScratchColor
    dust = matprops.Dust
    rust = matprops.Rust
    print('createLeather('+name+')');
    mat = getMaterial(name)
    
    
    if mesh.materials.get(mat.name) is None:
        mesh.materials.append(mat)
    #mesh.active_material=mat    
    shader = getShader(mat)
    bump = getNode(mat,'Bump','ShaderNodeBump')#getBump(mat)
    mat.node_tree.links.new(bump.outputs['Normal'],shader.inputs['Normal'])
    bump.location = shader.location + Vector((-300,-300))
    voronoi = getNode(mat,'Voronoi','ShaderNodeTexVoronoi')#getVoronoi(mat)
    mat.node_tree.links.new(voronoi.outputs['Distance'],bump.inputs['Height'])
    voronoi.location = bump.location+Vector((-300,0))
    voronoi2 = getNode(mat,'Voronoi2','ShaderNodeTexVoronoi')
    mat.node_tree.links.new(voronoi2.outputs['Position'],voronoi.inputs['Vector'])
    voronoi2.location = voronoi.location + Vector((-300,0))
    colorramp = getNode(mat,'ColorRamp','ShaderNodeValToRGB')
    mat.node_tree.links.new(voronoi.outputs['Color'],colorramp.inputs['Fac'])
    mat.node_tree.links.new(colorramp.outputs['Color'],shader.inputs['Base Color'])
    colorramp.location = shader.location + Vector((-300,0))
    mapping = getNode(mat,'Mapping','ShaderNodeMapping')
    mat.node_tree.links.new(mapping.outputs['Vector'],voronoi2.inputs['Vector'])
    mapping.location = voronoi2.location + Vector((-300,0))
    texCoord = getNode(mat,'TextureCoord','ShaderNodeTexCoord')
    mat.node_tree.links.new(texCoord.outputs['Object'],mapping.inputs['Vector'])
    texCoord.location = mapping.location + Vector((-300,0))   
    return mat  

def createMetal(mesh,matprops):#name,metalcol,basecol,grime,scratches,dust,grimecolor):
    name = matprops.MatBaseType
    metalcol = matprops.MetalColor
    basecol = matprops.MatBaseColor
    grime = matprops.Grime
    grimecolor = matprops.GrimeColor
    grimestrength = matprops.GrimeStrength
    scratches=matprops.Scratches
    scratchcolor=matprops.ScratchColor
    dust = matprops.Dust
    rust = matprops.Rust
    print('createMetal('+name+')');
    mat = getMaterial(name)
    
    
    if mesh.materials.get(mat.name) is None:
        mesh.materials.append(mat)
    #mesh.active_material=mat
    shader = getShader(mat)
    shader.inputs['Metallic'].default_value=1
    if metalcol != 'NONE':
        setShaderColor(shader,metalcol)
    else:
        shader.inputs['Base Color'].default_value = [basecol[0],basecol[1],basecol[2],1]
    
                               
                               
                               
    bump = getNode(mat,'Bump','ShaderNodeBump')#getBump(mat)
    bump.inputs['Strength'].default_value = 0.18

    mat.node_tree.links.new(bump.outputs['Normal'],shader.inputs['Normal'])    
    bump.location = shader.location + Vector((-300,-400))
    colorramp = getNode(mat,'ColorRamp','ShaderNodeValToRGB')
    colorramp.color_ramp.elements[1].position = 0.55
    mat.node_tree.links.new(colorramp.outputs['Color'],bump.inputs['Height'])    
    colorramp.location = bump.location + Vector((-300,0))
    wavTex = getNode(mat,'WaveTexture','ShaderNodeTexWave')
    wavTex.inputs['Scale'].default_value = 23
    wavTex.inputs['Distortion'].default_value=68
    mat.node_tree.links.new(wavTex.outputs['Color'],colorramp.inputs['Fac'])
    wavTex.location = colorramp.location + Vector((-300,0))
    mapping = getNode(mat,'Mapping','ShaderNodeMapping')
    mat.node_tree.links.new(mapping.outputs['Vector'],wavTex.inputs['Vector'])
    mapping.location = wavTex.location + Vector((-300,0))
    mixrgb = getNode(mat,'MixRGB','ShaderNodeMixRGB')
    mixrgb.inputs['Fac'].default_value=0.69
    mat.node_tree.links.new(mixrgb.outputs['Color'],mapping.inputs['Vector'])
    mixrgb.location = mapping.location + Vector((-300,0))
    noiseTex = getNode(mat,'NoiseTexture','ShaderNodeTexNoise')
    noiseTex.inputs['Detail'].default_value=16
    mat.node_tree.links.new(noiseTex.outputs['Color'],mixrgb.inputs['Color1'])
    noiseTex.location = mixrgb.location + Vector((-300,0))   
    texCoord = getNode(mat,'TextureCoord','ShaderNodeTexCoord')
    mat.node_tree.links.new(texCoord.outputs['Object'],noiseTex.inputs['Vector'])
    mat.node_tree.links.new(texCoord.outputs['Object'],mixrgb.inputs['Color2'])
    texCoord.location = noiseTex.location + Vector((-300,0))   
    #large dents
    bump2 = getNode(mat,'Bump2','ShaderNodeBump')
    bump2.inputs['Strength'].default_value = 0.25
    mat.node_tree.links.new(bump2.outputs['Normal'],bump.inputs['Normal'])
    bump2.location = bump.location + Vector((-300,-300))
    voronoiTex = getNode(mat,'Voronoi','ShaderNodeTexVoronoi')
    voronoiTex.distance = 'MINKOWSKI'
    mat.node_tree.links.new(voronoiTex.outputs['Distance'],bump2.inputs['Height'])
    voronoiTex.location = bump2.location+Vector((-300,0))
    mat.node_tree.links.new(texCoord.outputs['Object'],voronoiTex.inputs['Vector']) 
    for l in mat.node_tree.links:
        if l.to_socket == shader.inputs['Base Color']:
            mat.node_tree.links.remove(l)
      
    if grime:
        grimeGroup = getGrimeGroup()
        grimeGroupInstance = mat.node_tree.nodes.get('GrimeGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('GrimeGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')
        grimeGroupInstance.name = 'GrimeGroup'
        grimeGroupInstance.node_tree = grimeGroup
        
        mat.node_tree.links.new(grimeGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])
        grimeGroupInstance.inputs['Base Color'].default_value = shader.inputs['Base Color'].default_value
        grimeGroupInstance.inputs['Grime Color'].default_value= [grimecolor[0],grimecolor[1],grimecolor[2],1]
        grimeGroupInstance.inputs['Grime Strength'].default_value = 1- grimestrength
        grimeGroupInstance.location = shader.location+Vector((-300,0))
        mat.node_tree.links.new(mapping.outputs['Vector'],grimeGroupInstance.inputs['Vector'])
        #mat.node_tree.links.new(mapping.outputs['Vector'],grimeGroup.nodes.get('GrimeGroupInputs').outputs['Vector'])
    if scratches:
        scratchesGroup = getScratchesGroup()
        scratchGroupInstance = mat.node_tree.nodes.get('ScratchGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('scratchGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')
        scratchGroupInstance.name = 'ScratchGroup'
        scratchGroupInstance.node_tree = scratchesGroup        
        scratchGroupInstance.location = shader.location+Vector((-300,0))
        scratchGroupInstance.inputs['Base Color'].default_value = shader.inputs['Base Color'].default_value
        scratchGroupInstance.inputs['Scratch Color'].default_value = [scratchcolor[0],scratchcolor[1],scratchcolor[2],1]        
        if grime:
            grimeGroupInstance = mat.node_tree.nodes.get('GrimeGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('GrimeGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')            
            grimeGroupInstance.location = scratchGroupInstance.location+Vector((-300,0))
            mat.node_tree.links.new(grimeGroupInstance.outputs['Base Color'],scratchGroupInstance.inputs['Base Color'])                        
        mat.node_tree.links.new(scratchGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])


    if dust:
        dustGroup = getDustGroup()        
    return mat

def createBrick(mesh,matprops):#name,color1,color2,mortar,smoothness,grime,scratches,dust,grimecolor):
    name = matprops.MatBaseType



    grime = matprops.Grime
    grimecolor = matprops.GrimeColor
    grimestrength = matprops.GrimeStrength
    plasticsmoothness = matprops.PlasticSmoothness
    scratches=matprops.Scratches
    scratchcolor = matprops.ScratchColor
    dust = matprops.Dust
    rust = matprops.Rust
    color1=matprops.BrickColor1
    color2=matprops.BrickColor2
    mortar=matprops.BrickMortarColor
    smoothness=matprops.BrickSmoothness
    print('createBrick('+name+')');
    mat = getMaterial(name)
    
    
    if mesh.materials.get(mat.name) is None:
        mesh.materials.append(mat)
    #mesh.active_material=mat
    shader = getShader(mat)
    #setShaderColor(shader,color1)
    
                               
                               
                               
    bump = getNode(mat,'Bump','ShaderNodeBump')#getBump(mat)
    bump.inputs['Strength'].default_value = 0.8

    mat.node_tree.links.new(bump.outputs['Normal'],shader.inputs['Normal'])    
    bump.location = shader.location + Vector((-200,-400))
    brickTex = getNode(mat,'BrickTexture','ShaderNodeTexBrick')
    mat.node_tree.links.new(brickTex.outputs['Color'],shader.inputs['Base Color'])
    brickTex.location = shader.location + Vector((-1200,0))
    brickTex.inputs['Mortar'].default_value = [mortar[0],mortar[1],mortar[2],1]
    brickTex.inputs['Color1'].default_value = [color1[0],color1[1],color1[2],1]# [0.8,0.1,0.0,1]
    brickTex.inputs['Color2'].default_value = [color2[0],color2[1],color2[2],1]#[0.2,0.01,0.0,1]
    colorramp = getNode(mat,'ColorRamp1','ShaderNodeValToRGB')
    colorramp.color_ramp.elements[0].position = 0.077
    colorramp.color_ramp.elements[1].position = 0.632
    colorramp.color_ramp.elements[1].color = [color1[0],color1[1],color1[2],1]# [0.8,0.1,0.0,1]
    mat.node_tree.links.new(colorramp.outputs['Color'],brickTex.inputs['Color1'])
    colorramp.location = brickTex.location + Vector((-300,150))
    colorramp2 = getNode(mat,'ColorRamp2','ShaderNodeValToRGB')
    colorramp2.color_ramp.elements[0].position = 0.223
    colorramp2.color_ramp.elements[1].position = 0.855
    colorramp2.color_ramp.elements[1].color = [color2[0],color2[1],color2[2],1]#[0.2,0.01,0.0,1]
    mat.node_tree.links.new(colorramp2.outputs['Color'],brickTex.inputs['Color2'])
    colorramp2.location = brickTex.location + Vector((-300,-150))
    colorramp3 = getNode(mat,'ColorRamp3','ShaderNodeValToRGB')
    colorramp3.color_ramp.elements[0].position = 0.1
    colorramp3.color_ramp.elements[1].position = 0.8
    colorramp3.color_ramp.elements[1].color = [mortar[0],mortar[1],mortar[2],1]
    mat.node_tree.links.new(colorramp3.outputs['Color'],brickTex.inputs['Mortar'])
    colorramp3.location = brickTex.location+Vector((-300,-450))
    invert = getNode(mat,'Invert','ShaderNodeInvert')
    mat.node_tree.links.new(brickTex.outputs['Fac'],invert.inputs['Color'])
    mat.node_tree.links.new(invert.outputs['Color'],bump.inputs['Height'])
    invert.location = bump.location + Vector((-800,150))    
    whiteTex = getNode(mat,'WhiteNoise','ShaderNodeTexWhiteNoise')
    mat.node_tree.links.new(whiteTex.outputs['Value'],colorramp3.inputs['Fac'])
    whiteTex.location = colorramp3.location + Vector((-300,0))
    
    bump2 = getNode(mat,'Bump2','ShaderNodeBump')
    mat.node_tree.links.new(bump2.outputs['Normal'],bump.inputs['Normal'])
    bump2.location = bump.location + Vector((-200,-150))
    mixrgb = getNode(mat,'MixRGB','ShaderNodeMixRGB')
    mixrgb.blend_type='MULTIPLY'
    mixrgb.inputs['Fac'].default_value=1
    mat.node_tree.links.new(mixrgb.outputs['Color'],bump2.inputs['Height'])
    mixrgb.location = bump2.location+Vector((-200,0))
    mixrgbSmooth = getNode(mat,'MixRGBSmooth','ShaderNodeMixRGB')
    mixrgbSmooth.blend_type='MIX'
    mixrgbSmooth.inputs['Fac'].default_value=smoothness
    mat.node_tree.links.new(mixrgbSmooth.outputs['Color'],mixrgb.inputs['Color2'])
    mixrgbSmooth.location = mixrgb.location+Vector((-200,-250))
    colorramp4 = getNode(mat,'ColorRamp4','ShaderNodeValToRGB')
    colorramp4.color_ramp.elements[1].position = 0.22
    mat.node_tree.links.new(invert.outputs['Color'],mixrgb.inputs['Fac'])
    mat.node_tree.links.new(colorramp4.outputs['Color'],mixrgbSmooth.inputs['Color1'])
    colorramp4.location = mixrgbSmooth.location+Vector((-300,-250))
    

    mixrgb2 = getNode(mat,'MixRGB2','ShaderNodeMixRGB')
    mixrgb2.blend_type='MULTIPLY'
    mixrgb2.inputs['Fac'].default_value=0.9
    mat.node_tree.links.new(mixrgb2.outputs['Color'],colorramp4.inputs['Fac'])
    mixrgb2.location = colorramp4.location+Vector((-300,0))
    voronoi = getNode(mat,'Voronoi1','ShaderNodeTexVoronoi')
    voronoi.inputs['Scale'].default_value=55
    voronoi.feature = 'DISTANCE_TO_EDGE'
    mat.node_tree.links.new(voronoi.outputs['Distance'],mixrgb2.inputs['Color1'])
    voronoi.location = mixrgb2.location + Vector((-300,150))
    voronoi2 = getNode(mat,'Voronoi2','ShaderNodeTexVoronoi')
    voronoi2.inputs['Scale'].default_value=60
    voronoi2.feature = 'DISTANCE_TO_EDGE'
    mat.node_tree.links.new(voronoi2.outputs['Distance'],mixrgb2.inputs['Color2'])
    voronoi2.location = mixrgb2.location + Vector((-300,-150))
    mixrgb3 = getNode(mat,'MixRGB3','ShaderNodeMixRGB')
    mixrgb3.blend_type='MIX'
    mat.node_tree.links.new(invert.outputs['Color'],mixrgb3.inputs['Fac'])
    mat.node_tree.links.new(invert.outputs['Color'],mixrgb3.inputs['Color2'])
    mat.node_tree.links.new(mixrgb3.outputs['Color'],mixrgb.inputs['Color1'])
    mixrgb3.location = mixrgb.location +Vector((-200,0))
    voronoi3 = getNode(mat,'Voronoi3','ShaderNodeTexVoronoi')
    voronoi3.inputs['Scale'].default_value=500
    mat.node_tree.links.new(voronoi3.outputs['Distance'],mixrgb3.inputs['Color1'])
    voronoi3.location = mixrgb3.location +Vector((-300,0))
    noiseTex = getNode(mat,'NoiseTex','ShaderNodeTexNoise')
    noiseTex.inputs['Scale'].default_value=12.3
    noiseTex.inputs['Detail'].default_value=0
    noiseTex.inputs['Distortion'].default_value=2.2
    mat.node_tree.links.new(noiseTex.outputs['Color'],colorramp.inputs['Fac'])
    mat.node_tree.links.new(noiseTex.outputs['Color'],colorramp2.inputs['Fac'])
    noiseTex.location = colorramp.location + Vector((-300,-150))
    
    mapping = getNode(mat,'Mapping','ShaderNodeMapping')
    mat.node_tree.links.new(mapping.outputs['Vector'],noiseTex.inputs['Vector'])
    mat.node_tree.links.new(mapping.outputs['Vector'],whiteTex.inputs['Vector'])
    mat.node_tree.links.new(mapping.outputs['Vector'],voronoi.inputs['Vector'])
    mat.node_tree.links.new(mapping.outputs['Vector'],voronoi2.inputs['Vector'])
    mat.node_tree.links.new(mapping.outputs['Vector'],voronoi3.inputs['Vector'])
    mapping.location = noiseTex.location + Vector((-300,-300))
    mixrgb4 = getNode(mat,'MixRGB4','ShaderNodeMixRGB')
    mixrgb4.inputs['Fac'].default_value = 0.95
    mat.node_tree.links.new(mixrgb4.outputs['Color'],mapping.inputs['Vector'])
    mixrgb4.location = mapping.location + Vector((-300,0))
    noiseTex2 = getNode(mat,'NoiseTex2','ShaderNodeTexNoise')
    noiseTex2.inputs['Scale'].default_value = 2
    noiseTex2.inputs['Detail'].default_value=6
    noiseTex2.inputs['Distortion'].default_value=0
    mat.node_tree.links.new(noiseTex2.outputs['Color'],mixrgb4.inputs['Color1'])
    noiseTex2.location = mixrgb4.location + Vector((-300,150))
    mixrgb5 = getNode(mat,'MixRGB5','ShaderNodeMixRGB')
    mixrgb5.inputs['Fac'].default_value=0.95
    mat.node_tree.links.new(noiseTex2.outputs['Color'],mixrgb4.inputs['Color1'])
    mat.node_tree.links.new(mixrgb5.outputs['Color'],mixrgb4.inputs['Color2'])
    mat.node_tree.links.new(mixrgb5.outputs['Color'],noiseTex2.inputs['Vector'])
    mixrgb5.location = noiseTex2.location + Vector((-300,-300))
    noiseTex3 = getNode(mat,'NoiseTex3','ShaderNodeTexNoise')
    noiseTex3.inputs['Scale'].default_value=19
    noiseTex3.inputs['Detail'].default_value=6
    noiseTex3.inputs['Distortion'].default_value=0
    mat.node_tree.links.new(noiseTex3.outputs['Color'],mixrgb5.inputs['Color1'])
    noiseTex3.location = mixrgb5.location + Vector((-300,300))
    texCoord = getNode(mat,'TextureCoord','ShaderNodeTexCoord')
    mat.node_tree.links.new(texCoord.outputs['Object'],noiseTex3.inputs['Vector'])
    mat.node_tree.links.new(texCoord.outputs['Object'],mixrgb5.inputs['Color2'])
    texCoord.location = noiseTex3.location + Vector((-300,-300))   
    
    if grime:
        grimeGroup = getGrimeGroup()
        grimeGroupInstance = mat.node_tree.nodes.get('GrimeGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('GrimeGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')
        grimeGroupInstance.name = 'GrimeGroup'
        grimeGroupInstance.node_tree = grimeGroup
        mat.node_tree.links.new(brickTex.outputs['Color'],grimeGroupInstance.inputs['Base Color'])
        mat.node_tree.links.new(grimeGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])
        grimeGroupInstance.inputs['Grime Color'].default_value=[grimecolor[0],grimecolor[1],grimecolor[2],1]
        grimeGroupInstance.location = shader.location+Vector((-300,0))
        grimeGroupInstance.inputs['Grime Strength'].default_value =1- grimestrength
        mat.node_tree.links.new(texCoord.outputs['Object'],grimeGroupInstance.inputs['Vector'])
        #mat.node_tree.links.new(mapping.outputs['Vector'],grimeGroup.nodes.get('GrimeGroupInputs').outputs['Vector'])
    if scratches:
        scratchesGroup = getScratchesGroup()
        scratchGroupInstance = mat.node_tree.nodes.get('ScratchGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('scratchGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')
        scratchGroupInstance.name = 'ScratchGroup'
        scratchGroupInstance.node_tree = scratchesGroup        
        scratchGroupInstance.location = shader.location+Vector((-300,0))
        mat.node_tree.links.new(scratchGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])        
        scratchGroupInstance.inputs['Base Color'].default_value = shader.inputs['Base Color'].default_value
        scratchGroupInstance.inputs['Scratch Color'].default_value = [scratchcolor[0],scratchcolor[1],scratchcolor[2],1]        
        if grime:
            grimeGroupInstance = mat.node_tree.nodes.get('GrimeGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('GrimeGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')            
            grimeGroupInstance.location = scratchGroupInstance.location+Vector((-300,0))

            mat.node_tree.links.new(grimeGroupInstance.outputs['Base Color'],scratchGroupInstance.inputs['Base Color'])                        
        mat.node_tree.links.new(scratchGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])

    if dust:
        dustGroup = getDustGroup()       
        
    return mat
    
def createPlastic(mesh,matprops):#name,basecol,plasticsmoothness,grime,scratches,dust,grimecolor):
    name = matprops.MatBaseType    
    basecol = matprops.MatBaseColor
    grime = matprops.Grime
    grimecolor = matprops.GrimeColor
    grimestrength = matprops.GrimeStrength
    plasticsmoothness = matprops.PlasticSmoothness
    scratches=matprops.Scratches
    scratchcolor = matprops.ScratchColor
    dust = matprops.Dust
    rust = matprops.Rust
    print('createPlastic('+name+')');
    mat = getMaterial(name)
    
    
    if mesh.materials.get(mat.name) is None:
        mesh.materials.append(mat)
    shader = getShader(mat)
    #setShaderColor(shader,basecol)
    shader.inputs['Base Color'].default_value=[basecol[0],basecol[1],basecol[2],1]
    bump = getNode(mat,'Bump','ShaderNodeBump')#getBump(mat)
    bump.inputs['Strength'].default_value=0.01
    mat.node_tree.links.new(bump.outputs['Normal'],shader.inputs['Normal'])
    bump.location = shader.location + Vector((-300,-600))
    noiseTex = getNode(mat,'NoiseTexture','ShaderNodeTexNoise')
    noiseTex.inputs['Scale'].default_value=800
    noiseTex.inputs['Detail'].default_value=16
    noiseTex.inputs['Distortion'].default_value=0
    mat.node_tree.links.new(noiseTex.outputs['Color'],bump.inputs['Height'])
    noiseTex.location = bump.location + Vector((-300,0))
    mixrgb = getNode(mat,'MixRGB','ShaderNodeMixRGB')    
    mixrgb.inputs['Fac'].default_value=0.01
    #mixrgb.inputs['Color1'].default_value=plasticsmoothness
    mixrgb.blend_type = 'OVERLAY'
    mat.node_tree.links.new(mixrgb.outputs['Color'],shader.inputs['Roughness'])
    mixrgb.location = shader.location + Vector((-300,0))
    colorramp = getNode(mat,'ColorRamp','ShaderNodeValToRGB')
    colorramp.color_ramp.elements[0].position = 0.215
    mat.node_tree.links.new(colorramp.outputs['Color'],mixrgb.inputs['Color2'])    
    colorramp.location = mixrgb.location + Vector((-300,-150))
    noiseTex2 = getNode(mat,'NoiseTexture2','ShaderNodeTexNoise')
    noiseTex2.inputs['Scale'].default_value=40
    noiseTex2.inputs['Detail'].default_value=16
    noiseTex2.inputs['Distortion'].default_value=4
    mat.node_tree.links.new(noiseTex2.outputs['Fac'],colorramp.inputs['Fac'])
    noiseTex2.location = colorramp.location + Vector((-300,0))
    mathNode  = getNode(mat,'Math','ShaderNodeMath')
    mathNode.operation='ADD'
    mathNode.use_clamp=True
    mathNode.inputs[0].default_value=plasticsmoothness
    mathNode.inputs[1].default_value=0
    mat.node_tree.links.new(mathNode.outputs['Value'],mixrgb.inputs['Color1'])
    mathNode.location = mixrgb.location + Vector((-300,150))
    #value = getNode(mat,'Value','ShaderNodeValue')
    #value.default_value=plasticsmoothness
    #mat.node_tree.links.new(value.outputs['Value'],mixrgb.inputs['Color1'])   
    
    #value.location = mixrgb.location + Vector((-300,150))
    #mesh.active_material=mat
    #shader = getNode(mat,'MixShader','ShaderNodeMixShader')   
    #shaddiff = getNode(mat,'Diffuse','ShaderNodeBsdfDiffuse')
    #mat.node_tree.links.new(shaddiff.outputs['BSDF'],shader.inputs['Shader'])
    #shaddiff.location = shader.location + Vector((-300,300))
    #shadgloss = getNode(mat,'Glossy','ShaderNodeBsdfGlossy')
    #mat.node_tree.links.new(shadgloss.outputs['BSDF'],shader.inputs['Shader'])
    #shadgloss.location = shader.location+Vector((-300,-300))
    mapping = getNode(mat,'Mapping','ShaderNodeMapping')
    mat.node_tree.links.new(mapping.outputs['Vector'],noiseTex.inputs['Vector'])
    mat.node_tree.links.new(mapping.outputs['Vector'],noiseTex2.inputs['Vector'])
    mapping.location = noiseTex2.location + Vector((-300,150))
    texCoord = getNode(mat,'TextureCoord','ShaderNodeTexCoord')
    mat.node_tree.links.new(texCoord.outputs['Object'],mapping.inputs['Vector'])
    texCoord.location = mapping.location + Vector((-300,0))   
    
    for l in mat.node_tree.links:
        if l.to_socket == shader.inputs['Base Color']:
            mat.node_tree.links.remove(l)
    if grime:
        grimeGroup = getGrimeGroup()
        grimeGroupInstance = mat.node_tree.nodes.get('GrimeGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('GrimeGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')
        grimeGroupInstance.name = 'GrimeGroup'
        grimeGroupInstance.node_tree = grimeGroup
        grimeGroupInstance.inputs['Base Color'].default_value = [basecol[0],basecol[1],basecol[2],1]
        mat.node_tree.links.new(grimeGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])
        grimeGroupInstance.inputs['Grime Color'].default_value=[grimecolor[0],grimecolor[1],grimecolor[2],1]
        grimeGroupInstance.location = shader.location+Vector((-300,300))
        grimeGroupInstance.inputs['Grime Strength'].default_value =1- grimestrength        
        mat.node_tree.links.new(mapping.outputs['Vector'],grimeGroupInstance.inputs['Vector'])
    if scratches:
        scratchesGroup = getScratchesGroup()
        scratchesGroup = getScratchesGroup()
        scratchGroupInstance = mat.node_tree.nodes.get('ScratchGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('scratchGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')
        scratchGroupInstance.name = 'ScratchGroup'
        scratchGroupInstance.node_tree = scratchesGroup        
        scratchGroupInstance.location = shader.location+Vector((-300,0))
        mat.node_tree.links.new(scratchGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])        
        if grime:
            grimeGroupInstance = mat.node_tree.nodes.get('GrimeGroup') or mat.node_tree.nodes.new('ShaderNodeGroup')#mat.node_tree.get('GrimeGroupInstance') or mat.node_tree.new(type='ShaderNodeGroup')            
            grimeGroupInstance.location = scratchGroupInstance.location+Vector((-300,0))
            mat.node_tree.links.new(grimeGroupInstance.outputs['Base Color'],scratchGroupInstance.inputs['Base Color'])                        
        mat.node_tree.links.new(scratchGroupInstance.outputs['Base Color'],shader.inputs['Base Color'])
        mat.node_tree.links.new(scratchGroupInstance.outputs['Scratch Color'],scratchcolor)

    if dust:
        dustGroup = getDustGroup() 
    return mat 

def createFabric(mesh,matprops):#name,grime,dirt,dust,grimecolor):
    print('createFabric('+name+')');
    name = matprops.MatBaseType
    basecol = matprops.MatBaseColor    
    grime = matprops.Grime
    grimecolor = matprops.GrimeColor
    grimestrength = matprops.GrimeStrength
    scratches=matprops.Scratches
    dust = matprops.Dust
    rust = matprops.Rust
    smoothness=matprops.BrickSmoothness
    mat = getMaterial(name)
    
    
    if mesh.materials.get(mat.name) is None:
        mesh.materials.append(mat)
    shader = getShader(mat)
    mixrgb = getNode(mat,'MixRGB','ShaderNodeMixRGB')  
    mixrgb.blend_type = 'SUBTRACT'
    mixrgb.inputs['Fac'].default_value = 1
    mat.node_tree.links.new(mixrgb.outputs['Color'],shader.inputs['Base Color'])
    mixrgb.location = shader.location + Vector((-300,0))
    waveTex = getNode(mat,'WaveTexture','ShaderNodeTexWave')
    waveTex.inputs['Scale'].default_value = 40
    mat.node_tree.links.new(waveTex.outputs['Color'],mixrgb.inputs['Color1'])
    waveTex.location = mixrgb.location + Vector((-300,150))
    mapping = getNode(mat,'Mapping','ShaderNodeMapping')
    mapping.inputs['Scale'].default_value[0]=5
    mapping.inputs['Rotation'].default_value[2] = math.radians(45)
    mat.node_tree.links.new(mapping.outputs['Vector'],waveTex.inputs['Vector'])
    mapping.location = waveTex.location + Vector((-300,-150))
    texCoord = getNode(mat,'TextureCoord','ShaderNodeTexCoord')
    mat.node_tree.links.new(texCoord.outputs['UV'],mapping.inputs['Vector'])
    texCoord.location = mapping.location + Vector((-300,0))   
    waveTex2 = getNode(mat,'WaveTexture2','ShaderNodeTexWave')
    waveTex2.inputs['Scale'].default_value = 120
    mat.node_tree.links.new(waveTex2.outputs['Color'],mixrgb.inputs['Color2'])
    waveTex2.location = mixrgb.location + Vector((-300,-300))
    mapping2 = getNode(mat,'Mapping2','ShaderNodeMapping')
    
    mapping2.inputs['Rotation'].default_value[2] = math.radians(135)
    mat.node_tree.links.new(mapping2.outputs['Vector'],waveTex2.inputs['Vector'])
    mapping2.location = waveTex2.location + Vector((-300,-150))
    mat.node_tree.links.new(texCoord.outputs['UV'],mapping2.inputs['Vector'])
    #dump(mapping)
    return mat
        
def updateMaterial(self,context):
    print("updateMaterial()")
    scene = context.scene
    matprops = scene.matprops
    name = matprops.MatBaseType
    metalcol = matprops.MetalColor
    basecol = matprops.MatBaseColor
    plasticsmoothness = matprops.PlasticSmoothness
    grime = matprops.Grime
    grimecolor = matprops.GrimeColor
    scratches=matprops.Scratches
    dust=matprops.Dust
    mesh = context.object.data
    if name == 'MATMETAL':
        mat = createMetal(mesh,matprops)#name,metalcol,basecol,grime,scratches,dust,grimecolor)
    elif name == 'MATLEATHER':    
        mat = createLeather(mesh,matprops)#name,grime,scratches,dust,grimecolor)
    elif name == 'MATBRICK':
        color1=matprops.BrickColor1
        color2=matprops.BrickColor2
        mortar=matprops.BrickMortarColor
        smoothness=matprops.BrickSmoothness
        mat = createBrick(mesh,matprops)#name,color1,color2,mortar,smoothness,grime,scratches,dust,grimecolor)  
    elif name == 'MATPLASTIC':
        mat = createPlastic(mesh,matprops)#name,basecol,plasticsmoothness,grime,scratches,dust,grimecolor) 
    elif name == 'MATFAB':
        mat = createFabric(mesh,matprops)#name,grime,scratches,dust,grimecolor)        
    else:
        mat = createMetal(mesh,matprops)#name,metalcol,basecol,grime,scratches,dust,grimecolor)    
    if mat != None:    
        context.active_object.active_material=mat    
        #printNodeTree(mat)
    
def updateBaseColor(self,context):
    print('updateBaseColor()')
    print("updateMaterial()")
    scene = context.scene
    matprops = scene.matprops
    matprops.MetalColor='NONE'#override
    updateMaterial(self,context)    
    
class MatHelpProperties(PropertyGroup):
    

    MatBaseType: EnumProperty(
        name="BaseType:",
        description="Material Base Type.",
        items=[ ('MATMETAL', "Metal", ""),
                ('MATPLASTIC', "Plastic", ""),
                ('MATLEATHER', "Leather", ""),
                ('MATBRICK','Brick',''),
                ('MATFAB','Fabric','')
               ],
        update=updateMaterial       
               
        )
    MatBaseColor: FloatVectorProperty(name="BaseColor",
        subtype="COLOR",size=3,min=0.0,max=1,default=[0.83,0.69,0.22],
        update=updateBaseColor
    )
    MetalColor: EnumProperty(
        name="BaseColor:",
        description="Material Base Color.",
        items=[('NONE','None',""),
                ('GOLD','Gold',""),
                ('SILVER','Silver',''),
                ('BRONZE','Bronze',''),
                ('COPPER','Copper',''),
                ('ALUMINIUM','Aluminium',''),
                ('IRON','Iron',''),
                ('CHROMIUM','Chromium',''),
                ('NICKEL','Nickel',''),
                ('TITANIUM','Titanium',''),
                ('COBALT','Cobalt','')
                ],
        update=updateMaterial
    )        
    PlasticSmoothness: FloatProperty(        name="PlasticSmoothness",
        min=0.0,max=1,default=0.5,
        update=updateMaterial
    )
    BrickColor1: FloatVectorProperty(name="BrickColor1",
        subtype="COLOR",size=3,min=0.0,max=1,default=[0.8,0.1,0],
        update=updateMaterial
    )
    BrickColor2: FloatVectorProperty(name="BrickColor1",
        subtype="COLOR",size=3,min=0.0,max=1,default=[0.799,0.1,0.1],
        update=updateMaterial
    )
    BrickMortarColor: FloatVectorProperty(name="BrickMortarColor",
        subtype="COLOR",size=3,min=0.0,max=1,default=[0.5,0.5,0.5],
        update=updateMaterial
    )
    BrickSmoothness: FloatProperty(name="BrickSmoothness",
        min=0.0,max=1,default=0.5,
        update=updateMaterial
    )
    
    Grime: BoolProperty(name="Grime",
        description= "Add grime",default=False,
        update=updateMaterial
    )
    GrimeColor: FloatVectorProperty(name="GrimeColor",
        subtype="COLOR",size=3,min=0.0,max=1,default=[0.5,0.5,0.5],
        update=updateMaterial
    )
    GrimeStrength: FloatProperty(name="GrimeStrength",
        min=0.01,max=0.99,default=0.164,
        update=updateMaterial
    )
    Scratches: BoolProperty(name="Scratches",
        description= "Add scratches",default=False,
        update=updateMaterial
    )
    ScratchColor: FloatVectorProperty(name="ScratchColor",
        subtype="COLOR",size=3,min=0.0,max=1,default=[0.5,0.5,0.5],
        update=updateMaterial
    )
    Dust: BoolProperty(name="Dust",
        description= "Add dust",default=False,
        update= updateMaterial
    )    
    Rust: BoolProperty(name="Rust",
        description="Add rust",default=False,
        update=updateMaterial
    )

class NODE_MatHelp_Create(bpy.types.Operator):
    bl_idname = 'wm.mathelp_create'
    bl_label = 'Material Workflow'
    bl_descriptions = 'Metalic or Non-Metalic workflow'
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(clss,context):
        return True
    
    def execute(self,context):
        print('NODE_MatHelp_Create execute()')
        scene = context.scene
        matprops = scene.matprops
        name = matprops.MatBaseType
        metalcol = matprops.MetalColor
        matprops.MatBaseColor=[0.83,0.69,0.22]
        basecol = matprops.MatBaseColor
        mesh = context.object.data
        grime = matprops.Grime
        matprops.GrimeColor = [0.5,0.5,0.5]
        grimecolor = matprops.GrimeColor
        matprops.GrimeStrength=0.164
        grimestrength = matprops.GrimeStrength
        matprops.PlasticSmoothness=0.5
        plasticsmoothness = matprops.PlasticSmoothness
        scratches=matprops.Scratches
        dust = matprops.Dust
        rust = matprops.Rust
        matprops.BrickColor1 = [0.8,0.1,0]
        matprops.BrickColor2 = [0.799,0.1,0.1]
        matprops.BrickMortarColor = [0.5,0.5,0.5]
        matprops.BrickSmoothness=0.5
        color1=matprops.BrickColor1
        color2=matprops.BrickColor2
        mortar=matprops.BrickMortarColor
        smoothness=matprops.BrickSmoothness
        print(mesh)
        if name == 'MATMETAL':
            mat = createMetal(mesh,matprops)#metal,basecol,grime,scratches,dust,grimecolor,grimestrength)
        elif name == 'MATLEATHER':    
            mat = createLeather(mesh,matprops)#grime,scratches,dust,grimecolor,grimestrength)
        elif name == 'MATPLASTIC':
            mat = createPlastic(mesh,matprops)#basecol,plasticsmoothness,grime,scratches,dust,grimecolor,grimestrength)    
        elif name == 'MATBRICK':
           
            mat = createBrick(mesh,matprops)#color1,color2,mortar,smoothness,grime,scratches,dust,grimecolor,grimestrength)
        elif name == 'MATFAB':
            mat = createFabric(mesh,matprops)#grime,scratches,dust,grimecolor)        
        else:
            mat = createMetal(mesh,matprops)#'GOLD',basecol,grime,scratches,dust,grimecolor)    
        #printNodeTree(mat)
        return {'FINISHED'}
    
    
class NODE_PT_MatHelpPanel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_label = 'Material Helper'
    
    def draw(self,context):
        scene = context.scene
        matprops = scene.matprops
        layout = self.layout
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        
        row.operator('wm.mathelp_create',text='Create')
        row = layout.row(align=True)
        row.alignment = 'EXPAND'  
        row = layout.row(align=True)  
        row.prop(matprops,'MatBaseType',text='Type')
        type = matprops.MatBaseType
        if type == 'MATMETAL':
            layout.label(text='Metal Colors:')
            row = layout.row(align=True)
            row.prop(matprops,'MetalColor',text='Preset')  
            row = layout.row(align=True)
            row.prop(matprops,'MatBaseColor',text='Color')
        elif type == 'MATPLASTIC':
            row=layout.row()
            row.prop(matprops,'MatBaseColor',text='Color')
            row=layout.row()
            row.prop(matprops,'PlasticSmoothness',text='Smoothness')
        elif type == 'MATBRICK':
            layout.label(text='Brick Colors:')
            row = layout.row(align=True)
            row.prop(matprops,'BrickColor1',text='Color1')
            row.prop(matprops,'BrickColor2',text='Color2')
            row=layout.row()
            row.prop(matprops,'BrickMortarColor',text='Mortar Color')
            row=layout.row()
            row.prop(matprops,'BrickSmoothness',text='Brick Smoothness')

        row = layout.row()
        row.prop(matprops,'Grime',text='Grime')    
        row = layout.row()
        row.prop(matprops,'GrimeColor',text='Color')
        row = layout.row()
        row.prop(matprops,'GrimeStrength',text='Strength')
        row = layout.row()
        row.prop(matprops,'Scratches',text='Scratches')    
        row = layout.row()
        row.prop(matprops,'ScratchColor',text='Color')
        row = layout.row()
        row.prop(matprops,'Dust',text='Dust')  
        row = layout.row()
        row.prop(matprops,'Rust',text='Rust')  
        

        #layout.prop(matprops, "MatBaseType", text="Type") 
        
        #layout.prop(matprops,"MatBaseColor",text="Color")
        
classes = (
    MatHelpProperties,
    NODE_MatHelp_Create,
    NODE_PT_MatHelpPanel
)        
        
def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.matprops = PointerProperty(type=MatHelpProperties)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.matprops

if __name__ == "__main__":
    register()        