bl_info = {
    "name": "Mosaic game",
    "author": "nikitron",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Tool Shelf > SV > Mosaic",
    "description": "Play and win",
    "warning": "",
    "wiki_url": "https://github.com/nortikin/nikitron_tools/wiki",
    "tracker_url": "https://github.com/nortikin/nikitron_tools/issues",
    "category": "Misc"}


import bpy
import random
from bpy.props import IntProperty

# Глобальное хранилище layout
button_data = []
Рекорд = 0
Шаги = 0


class MosaicButtonPanel(bpy.types.Panel):
    bl_label = "Mosaic Buttons"
    bl_idname = "PT_MosaicButtonPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SV'

    def draw(self, context):
        global button_data
        layout = self.layout

        # Инициализация при первом открытии
        if not button_data:
            button_data = self.generate_button_layout()

        # Создаем основную сетку через column/row
        main_col = layout.column(align=True)

        # 5 строк по 5 ячеек
        for row in range(10):
            row_layout = main_col.row(align=True)
            for col in range(10):
                cell = button_data[row * 10 + col]

                if cell['used']:
                    continue

                # Создаем кнопку с нужными размерами
                btn = row_layout.operator(
                    'wm.mosaic_button',
                    text=f"{row*10+col}({cell['w']}x{cell['h']})",
                    depress=cell['depress']
                )
                btn.button_id = cell['id']

                # Масштабируем по ширине
                row_layout.separator()
                row_layout.scale_x = cell['w']

                # Для вертикального масштабирования используем пустые строки
                for _ in range(cell['h'] - 1):
                    row_layout.separator()

    def generate_button_layout(self):
        """Генерирует фиксированный layout кнопок"""
        layout = []
        occupied = [False] * 100  # 5x5 grid

        for i in range(100):
            if occupied[i]:
                layout.append({'used': True})
                continue

            row = i // 10
            col = i % 10

            # Максимальные размеры с учетом границ
            max_w = min(3, 10 - col)
            max_h = min(3, 10 - row)

            w = random.randint(1, max_w)
            h = random.randint(1, max_h)
            if not occupied[i] and i==0:
                depress = False
            else:
                depress = True #random.choice([True, True])

            # Помечаем занятые ячейки
            for r in range(row, row + h):
                for c in range(col, col + w):
                    if r * 10 + c < 100:
                        occupied[r * 10 + c] = True

            layout.append({
                'used': False,
                'id': i,
                'w': w,
                'h': h,
                'depress': depress
            })
        #layout = [l for l in layout if l['used'] != True]
        return layout

class WM_OT_MosaicButton(bpy.types.Operator):
    bl_idname = "wm.mosaic_button"
    bl_label = "Mosaic Button"

    button_id: IntProperty()

    def execute(self, context):
        global button_data
        global Рекорд
        global Шаги
        button_data[self.button_id]['depress'] = True
        for t in range(random.choice((2,3,5))):
            random.choice(button_data)['depress'] = False
        win = True
        for w in button_data:
            if w['used'] == False:
                if w['depress'] == False:
                    win = False
                    break
        if win:
            if Шаги > Рекорд:
                self.report({'INFO'}, f'Вы выиграли и поставили новый рекорд {Шаги} шагов!')
                Рекрод = Шаги
                Шаги = 0
            else:
                self.report({'INFO'}, 'Вы просто выиграли!')
                Шаги = 0

        else:
            Шаги += 1
        print(f"Pressed button {self.button_id}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(WM_OT_MosaicButton)
    bpy.utils.register_class(MosaicButtonPanel)

def unregister():
    bpy.utils.unregister_class(MosaicButtonPanel)
    bpy.utils.unregister_class(WM_OT_MosaicButton)


if __name__ == "__main__":
    register()
