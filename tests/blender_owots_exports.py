"""Blender 5.2 native OWOTS skeleton/chain export and save/reopen acceptance."""
import sys,importlib,json
from pathlib import Path
import bpy,addon_utils
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--samples',type=Path,required=True,help='Extracted OWOTS tree containing natives/')
parser.add_argument('--mesh',type=Path,required=True,help='Original ch001_00_00.mesh.260209350')
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--addon-root',type=Path,default=Path(__file__).resolve().parents[2])
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
root=args.addon_root.resolve();sys.path.insert(0,str(root))
out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
samples=args.samples.resolve();report={}
for addon in ('RE-Mesh-Editor-main','RE-Chain-Editor-main'):
 addon_utils.enable(addon,default_set=True)
 assert Path(importlib.import_module(addon).__file__).resolve().is_relative_to(root)
chain=importlib.import_module('RE-Chain-Editor-main')
bpy.context.preferences.addons['RE-Mesh-Editor-main'].preferences.showConsole=False
sk=importlib.import_module('RE-Mesh-Editor-main.modules.fbxskel.file_re_fbxskel')
report['blender']=bpy.app.version_string
report['fbxskel']=[]
for p in sorted((samples/'natives/stm/art/model/character/ch0').rglob('*.fbxskel.7'))[:3]:
 if 'export' in str(p):continue
 assert bpy.ops.re_fbxskel.importfile(filepath=str(p))=={'FINISHED'}
 arm=bpy.context.active_object
 target=out/'export'/p.name;target.parent.mkdir(exist_ok=True)
 assert bpy.ops.re_fbxskel.exportfile(filepath=str(target),filename_ext='.7',targetArmature=arm.name)=={'FINISHED'}
 a,b=sk.readFBXSkel(str(p)),sk.readFBXSkel(str(target))
 assert [(x.boneName,x.parentIndex,x.segmentScaling) for x in a.boneEntryList]==[(x.boneName,x.parentIndex,x.segmentScaling) for x in b.boneEntryList]
 from mathutils import Matrix,Vector,Quaternion
 max_error=0
 for x,y in zip(a.boneEntryList,b.boneEntryList):
  def mat(z):return Matrix.LocRotScale(Vector(z.translation),Quaternion((z.rotation[3],*z.rotation[:3])),Vector(z.scale))
  err=max(abs(v-w) for r,s in zip(mat(x),mat(y)) for v,w in zip(r,s));max_error=max(max_error,err)
 assert max_error<1e-4,max_error
 report['fbxskel'].append({'name':p.name,'bones':len(a.boneEntryList),'max_transform_error':max_error})
 bpy.data.objects.remove(arm,do_unlink=True)
p=args.mesh.resolve()
assert bpy.ops.re_mesh.importfile(directory=str(p.parent),files=[{'name':p.name}],loadMaterials=False,importAllLODs=False)=={'FINISHED'}
arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
p=next((samples/'natives').rglob('ch001_00_00.chain2.17'))
assert bpy.ops.re_chain2.importfile(filepath=str(p),targetArmature=arm.data.name,importUnknowns=True)=={'FINISHED'}
c=bpy.context.scene.re_chain_toolpanel.chainCollection
assert bpy.ops.re_chain2.exportfile(filepath=str(out/'export'/p.name),filename_ext='.17',targetCollection=c.name)=={'FINISHED'}
ch=importlib.import_module('RE-Chain-Editor-main.modules.file_re_chain2')
a,b=ch.readREChain2(str(p)),ch.readREChain2(str(out/'export'/p.name))
assert a.Header.chainGroupCount==b.Header.chainGroupCount
assert [g.nodeCount for g in a.ChainGroupList]==[g.nodeCount for g in b.ChainGroupList]
report['chain2']={'groups':b.Header.chainGroupCount,'nodes':sum(g.nodeCount for g in b.ChainGroupList),'settings':b.Header.chainSettingsCount,'version':b.Header.version}

# Check native fields, allowing the equivalent quaternion q/-q representation.
for x,y in zip(a.ChainGroupList,b.ChainGroupList):
 assert x.terminateNodeNameHash==y.terminateNodeNameHash
 for u,v in zip(x.nodeList,y.nodeList):
  assert u.jointHash==v.jointHash and u.constraintJntNameHash==v.constraintJntNameHash
  q=lambda n:Quaternion((n.angleLimitDirectionW,n.angleLimitDirectionX,n.angleLimitDirectionY,n.angleLimitDirectionZ))
  assert abs(abs(q(u).normalized().dot(q(v).normalized()))-1)<1e-5
assert a.Header.wilds_unkn0==b.Header.wilds_unkn0
assert [l.nodeCount for l in a.ChainLinkList]==[l.nodeCount for l in b.ChainLinkList]
report['free_links']=[]
import struct
free_sources=[p for p in (samples/'natives').rglob('*.chain2.17') if p.read_bytes()[94]]
for index,p in enumerate(p for p in free_sources if p.name == "ch001_00_01_mantchange.chain2.17"):
 # Keep the imported mesh armature; import unknown hashes preserves links to
 # bones from other skeleton resources without inventing bone names.
 assert bpy.ops.re_chain2.importfile(filepath=str(p),targetArmature=arm.data.name,importUnknowns=True)=={'FINISHED'}
 c=bpy.context.scene.re_chain_toolpanel.chainCollection
 cname=c.name
 stored=c['REChain2FreeLinks']
 if index==0:
  bpy.ops.wm.save_as_mainfile(filepath=str(out/'acceptance.blend'))
  bpy.ops.wm.open_mainfile(filepath=str(out/'acceptance.blend'))
  c=bpy.data.collections[cname]
  arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
  assert c['REChain2FreeLinks']==stored
 target=out/'export'/p.name
 assert bpy.ops.re_chain2.exportfile(filepath=str(target),filename_ext='.17',targetCollection=c.name)=={'FINISHED'}
 native, exported=ch.readREChain2(str(p)),ch.readREChain2(str(target))
 assert [(l.parameters,l.nodes) for l in native.FreeLinkList]==[(l.parameters,l.nodes) for l in exported.FreeLinkList]
 assert native.Header.freeLinkCount==exported.Header.freeLinkCount
 assert native.Header.freeLinkJoint==exported.Header.freeLinkJoint
 assert [g.terminateNodeNameHash for g in native.ChainGroupList]==[g.terminateNodeNameHash for g in exported.ChainGroupList]
 assert [g.nodeCount for g in native.ChainGroupList]==[g.nodeCount for g in exported.ChainGroupList]
 report['free_links'].append({'name':p.name,'free_links':len(exported.FreeLinkList)})
(out/'blender_report.json').write_text(json.dumps(report,indent=2))
print('OWOTS_EXPORT_ACCEPT_PASS',json.dumps(report))


