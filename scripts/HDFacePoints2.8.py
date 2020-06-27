import bpy
import socket
import bmesh
import math
from mathutils import Vector
from mathutils import Matrix
from mathutils import Euler

def set_bone_location(ob_name,vec,empty):
    arm_data = bpy.data.armatures['Head']        
    arm_ob = bpy.data.objects['Head']    
        
    
        
    if arm_data.edit_bones.get(ob_name) is None:
        print('Creating new bone ',ob_name)
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT',toggle=False)
            bpy.ops.object.mode_set(mode='EDIT',toggle=False)
        arm_ob.select_set(True)                            
        bone = arm_data.edit_bones.new(ob_name)
        if arm_data.edit_bones.get('HeadPivot') is None or ob_name == 'HeadPivot':
            bone.head = (vec.x,vec.y,vec.z)
            bone.tail = (vec.x,vec.y+0.1,vec.z)
        else:
            HeadPivot = arm_data.edit_bones['HeadPivot']        
                
            bone.head = (HeadPivot.head[0]+vec.x,HeadPivot.head[1]+vec.y,HeadPivot.head[2]+vec.z)
            bone.tail = (HeadPivot.tail[0]+vec.x,HeadPivot.tail[1]+vec.y,HeadPivot.tail[2]+vec.z)
        if bpy.context.object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='OBJECT',toggle=False)
            bpy.ops.object.mode_set(mode='POSE',toggle=False)    
        bone = arm_ob.pose.bones[ob_name]  
        print('Creation bone constraint.')  
        constraint = bone.constraints.new('COPY_LOCATION')
        constraint.target = empty
    else:
        bone = arm_data.edit_bones[ob_name]            
    
    
    
    #if bpy.context.object.mode != 'POSE':
     #   print('Setting pose mode')
    #    bpy.ops.object.mode_set(mode='OBJECT',toggle=False)
    #    bpy.ops.object.mode_set(mode='POSE',toggle=False)    
            
    #pose_bone = arm_ob.pose.bones[ob_name]        
        
    #if(bpy.context.scene.tool_settings.use_keyframe_insert_auto):
     #       pose_bone.keyframe_insert(data_path="location")        

def set_location(objects, ob_name, vec, originals):

    if ob_name in objects.keys():
        if ob_name not in originals.keys():
            originals[ob_name] = objects[ob_name].location.copy()

        objects[ob_name].location = vec
        
        if(bpy.context.scene.tool_settings.use_keyframe_insert_auto):
            objects[ob_name].keyframe_insert(data_path="location")
            
    else:
        print('Creating new empty ',ob_name)
        o = bpy.data.objects.new("empty", None)
        #2.79
        #bpy.context.scene.objects.link(o)        	
        #o.empty_draw_size=0.2
        #o.empty_draw_type='PLAIN_AXES'
        #2.8x		
        data = bpy.data
        collection = data.collections['Collection']
        #HDFacePoints = collection.objects['HDFacePoints']
        HeadPivot = collection.objects['HeadPivot']
        #o.parent = HDFacePoints
        o.parent = HeadPivot
        #face_obj.link(o)
        collection.objects.link(o);
        o.empty_display_size = 0.2
        o.empty_display_type = 'PLAIN_AXES'        
        o.name = ob_name
        o.location = vec

        if(bpy.context.scene.tool_settings.use_keyframe_insert_auto):
            objects[ob_name].keyframe_insert(data_path="location")
        
        set_bone_location(ob_name,vec,o)
        

class HDFacePointsReceiver2():
    
    location_dict = {}
    
    def __init__(self, DGRAM_PORT):
        print("Setting up socket in __init__")
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.sock.setblocking(0)
        self.sock.bind(("127.0.0.1",DGRAM_PORT))
        print("HDFacePointsReceiver socket open and listening.");
       
        
    
    def __del__(self):
        self.sock.close();
        print("HDFacePointsReceiver socket closed.");
        
    def buildContainerEmpty(self):
        data = bpy.data
        collection = data.collections['Collection']

        #if collection.objects.get('HDFacePoints') is None:
        #    HDFacePoints = bpy.data.objects.new('empty',None)
        #    HDFacePoints.name = 'HDFacePoints'
        #    collection.objects.link(HDFacePoints)
        #else:
        #    HDFacePoints = collection.objects['HDFacePoints']
            
        #if HDFacePoints.empty_display_type != 'CONE':
        #    HDFacePoints.empty_display_type = 'CONE'    
        #loc = Vector([0.0,-2.5,1.75])
        #if HDFacePoints.location != loc:
        #    HDFacePoints.location=loc
            
        #rot = Vector([math.radians(180.0),0.0,0.0])
        #if HDFacePoints.rotation_euler != rot:
        #    HDFacePoints.rotation_euler = rot  
            
        if collection.objects.get('HeadPivot') is None:
            HeadPivot = bpy.data.objects.new('empty',None)
            HeadPivot.name = 'HeadPivot'
            collection.objects.link(HeadPivot)
        else:
            HeadPivot = collection.objects['HeadPivot']
        HeadPivot.empty_display_size = 0.2
        HeadPivot.empty_display_type = 'PLAIN_AXES'        
        #HeadPivot.parent = HDFacePoints
        
        
        
        
        if bpy.data.armatures.get('Head') is None:
            print('Creating new Head armature')
            arm_data = bpy.data.armatures.new('Head')
        else:
            arm_data = bpy.data.armatures['Head']
    
        if bpy.data.objects.get('Head') is None:
            print('Creating new Head object')
            arm_ob = bpy.data.objects.new('Head',arm_data)
            collection.objects.link(arm_ob)
        else:
            arm_ob = bpy.data.objects['Head']
    
        bpy.context.view_layer.objects.active = arm_ob    
        
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT',toggle=False)
            bpy.ops.object.mode_set(mode='EDIT',toggle=False)
    
    
        arm_ob.select_set(True)
            
        
            
            

            
        
                              
        
        
    def run(self, objects, set_location_func):
        
        
        self.buildContainerEmpty()
        
        apply_location_dic = {}
        
        receive= True
        
        sync = False
        
        try:
            data = self.sock.recv(1024)
            #print('Received: ', data)
        except socket.error as e:
            print(e)
            data = None
            receive = False
            
        buff = data
        eul = Euler((math.radians(-90.0),math.radians(180.0),0.0),'XYZ')
        while(receive):
            data = buff
            print(data)
            parts = data.decode("utf-8").split(":")
            facepoint = parts[0]
            print(facepoint)
            coords = parts[1].split(",")
            xcoord = float(coords[0])
            ycoord = float(coords[1])
            zcoord = float(coords[2])
            zcoord = zcoord-0.5
            print('X: ',xcoord,' Y: ', ycoord, ' Z: ', zcoord)
            v2 = Vector([xcoord,ycoord,zcoord])
            if facepoint != 'HeadPivot':
                v2.rotate(eul)
            
            self.location_dict[facepoint] = v2
            
            
            try:
                buff = self.sock.recv(1024)
                print('Received:', buff)
            except socket.error as e:
                break
            
        for key, value in self.location_dict.items():
            #print('Key: ', key, ' Value: ', value)
            set_location_func(objects, key, value, self.location_dict)
            
            
class HDFacePoints_Start(bpy.types.Operator):
    bl_idname = "wm.hdfacepoints_start"
    bl_label = "HDFacePoints Start"
    bl_description = "Start receiving data from HDFacePoints app"
    bl_options = {'REGISTER'}
    
    enabled = False
    receiver = None
    timer = None
    
    def modal(self, context, event):
        if event.type == 'ESC' or not __class__.enabled:
            return self.cancel(context)
        
        if event.type == 'TIMER':
            self.receiver.run(bpy.data.objects, set_location)
            
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        __class__.enabled = True
        print('Enabled: ',self.enabled, __class__.enabled,HDFacePoints_Start.enabled)
        self.receiver = HDFacePointsReceiver2(7000)
        
        context.window_manager.modal_handler_add(self)
        self.timer = context.window_manager.event_timer_add(1/context.scene.render.fps,window=context.window)
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        __class__enabled=False
        context.window_manager.event_timer_remove(self.timer)
        
        del self.receiver
        
        return {'CANCELLED'}
    
    @classmethod
    def disable(cls):
        if cls.enabled:
            cls.enabled= False
            
            
            
class HDFacePoints_Stop(bpy.types.Operator):
    bl_idname = "wm.hdfacepoints_stop"
    bl_label = "HDFacePoints Stop"
    bl_descriptions = "Stop receiving data from HDFacePoints app"
    bl_options = {'REGISTER'}
    print('HDFacePoints_Stop')
    def execute(self,context):
        HDFacePoints_Start.disable()
        return {'FINISHED'}
    
class VIEW3D_PT_HDFacePointsPanel(bpy.types.Panel):
    print('Creating tab for HDFacePoints')
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_label = "HDFacePoints receiver"
    
    def draw(self,context):
        #print('HDFacePoints draw')
        layout = self.layout
        row = layout.row()
        
        #row.enabled = not HDFacePoints_Start.enabled
        #print('VIEW3D_PT_HDFacePointsPanel Enabled: ',HDFacePoints_Start.enabled)
        if(HDFacePoints_Start.enabled):
            row.operator('wm.hdfacepoints_stop',text = "Stop")
        else:
            row.operator('wm.hdfacepoints_start',text = "Start")
            
def register():
    bpy.utils.register_class(HDFacePoints_Start)
    bpy.utils.register_class(HDFacePoints_Stop)
    bpy.utils.register_class(VIEW3D_PT_HDFacePointsPanel)
    
def unregister():
    bpy.utils.unregister_class(HDFacePoints_Start)
    bpy.utils.unregister_class(HDFacePoints_Stop)
    bpy.utils.unregister_class(VIEW3D_PT_HDFacePointsPanel)
    
if __name__ == "__main__":
    register()
        


    
        
        
        
        
        
            