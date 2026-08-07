#!/usr/bin/env python3
"""Apply ballet app note itemization + movement picker fixes to index.html."""
import re, sys

SRC = "/app/data/所有对话/主对话/ballet-app/index.html"
with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---------------------------------------------------------------
# 1) Add new CSS styles after mv-picker-done block
# ---------------------------------------------------------------
old_css_block = """        .mv-picker-done:active { opacity: 0.8; }

        /* Add movement modal form */"""

new_css_block = """        .mv-picker-done:active { opacity: 0.8; }

        /* Note item list (for course / self training notes) */
        .note-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .note-item {
            background: var(--pink-50);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 10px;
            position: relative;
        }
        .note-item textarea {
            width: 100%;
            padding: 8px 10px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 13px;
            background: white;
            min-height: 60px;
            resize: vertical;
            font-family: inherit;
            box-sizing: border-box;
        }
        .note-item textarea:focus { outline: none; border-color: var(--pink-300); }
        .note-item-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 8px;
        }
        .note-item-pick {
            font-size: 12px;
            color: var(--pink-500);
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            background: white;
            border: 1px dashed var(--pink-300);
        }
        .note-item-del {
            font-size: 12px;
            color: #D4888A;
            cursor: pointer;
            padding: 4px 8px;
        }
        .note-item-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-top: 6px;
        }
        .note-item-tag {
            padding: 2px 6px;
            background: var(--pink-100);
            color: var(--pink-600);
            border-radius: 6px;
            font-size: 10px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 3px;
        }
        .note-item-tag .remove {
            cursor: pointer;
            opacity: 0.6;
        }
        .note-add-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background: var(--pink-100);
            color: var(--pink-600);
            border: 1px dashed var(--pink-300);
            border-radius: 10px;
            font-size: 13px;
            text-align: center;
            cursor: pointer;
            margin-top: 8px;
        }
        .note-add-btn:active { opacity: 0.8; }

        /* Movement picker overlay sits above main modal */
        #mv-picker-overlay { z-index: 2500; }

        /* Toast */
        .toast {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.75);
            color: white;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 14px;
            z-index: 9999;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .toast.show { opacity: 1; }

        /* Add movement modal form */"""

assert old_css_block in html, "CSS anchor not found"
html = html.replace(old_css_block, new_css_block, 1)
print("✅ CSS added")

# ---------------------------------------------------------------
# 2) Replace course notes textarea area with note list + add button
# ---------------------------------------------------------------
old_course_notes_html = """                        <div class="form-group">
                            <label>学习笔记</label>
                            <textarea id="course-notes" rows="4" placeholder="笔记内容"></textarea>
                        </div>
                        <div class="form-group">
                            <label>笔记照片</label>
                            <div class="photo-upload" id="course-notes-photos">
                                <label class="photo-add-btn" for="photo-input-course-notes"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></label>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>关联动作</label>
                            <div class="mv-picker-trigger" id="course-mv-trigger" onclick="openMovementPicker('course')">
                                <span id="course-mv-placeholder">点击选择关联动作...</span>
                            </div>
                        </div>"""

new_course_notes_html = """                        <div class="form-group">
                            <label>学习笔记</label>
                            <div class="note-list" id="course-notes-list"></div>
                            <button type="button" class="note-add-btn" onclick="addNoteItem('course')">+ 添加一条笔记</button>
                        </div>
                        <div class="form-group">
                            <label>笔记照片</label>
                            <div class="photo-upload" id="course-notes-photos">
                                <label class="photo-add-btn" for="photo-input-course-notes"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></label>
                            </div>
                        </div>"""

assert old_course_notes_html in html, "Course notes HTML not found"
html = html.replace(old_course_notes_html, new_course_notes_html, 1)
print("✅ Course notes form replaced")

# ---------------------------------------------------------------
# 3) Replace self-notes textarea + linked movements area
# ---------------------------------------------------------------
old_self_notes_html = """                        <div class="form-group">
                            <label>训练笔记</label>
                            <textarea id="self-notes" rows="4" placeholder="笔记内容"></textarea>
                        </div>
                        <div class="form-group">
                            <label>笔记照片</label>
                            <div class="photo-upload" id="self-notes-photos">
                                <label class="photo-add-btn" for="photo-input-self-notes"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></label>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>关联动作</label>
                            <div class="mv-picker-trigger" id="self-mv-trigger" onclick="openMovementPicker('self')">
                                <span id="self-mv-placeholder">点击选择关联动作...</span>
                            </div>
                        </div>"""

new_self_notes_html = """                        <div class="form-group">
                            <label>训练笔记</label>
                            <div class="note-list" id="self-notes-list"></div>
                            <button type="button" class="note-add-btn" onclick="addNoteItem('self')">+ 添加一条笔记</button>
                        </div>
                        <div class="form-group">
                            <label>笔记照片</label>
                            <div class="photo-upload" id="self-notes-photos">
                                <label class="photo-add-btn" for="photo-input-self-notes"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></label>
                            </div>
                        </div>"""

assert old_self_notes_html in html, "Self notes HTML not found"
html = html.replace(old_self_notes_html, new_self_notes_html, 1)
print("✅ Self notes form replaced")

# ---------------------------------------------------------------
# 4) Remove mv-picker-note textarea block inside picker modal
#    (since each note has its own text, picker only picks movements)
# ---------------------------------------------------------------
old_picker_note = """                <div class="mv-picker-note">
                    <label>要点笔记（将追加到动作的要点列表）</label>
                    <textarea id="mv-picker-note" placeholder="记录本节课关于所选动作的要点..."></textarea>
                </div>
                <button class="mv-picker-done" onclick="confirmMovementPicker()">确定</button>"""

new_picker_bottom = """                <button class="mv-picker-done" onclick="confirmMovementPicker()">确定</button>"""

assert old_picker_note in html, "Picker note block not found"
html = html.replace(old_picker_note, new_picker_bottom, 1)
print("✅ Picker note textarea removed")

# ---------------------------------------------------------------
# 5) Add toast element before mv-picker-overlay
# ---------------------------------------------------------------
old_toast_anchor = """        <!-- Movement Picker Modal -->
        <div class="modal-overlay" id="mv-picker-overlay" onclick="closeMovementPickerOverlay(event)">"""

new_toast_anchor = """        <!-- Toast -->
        <div class="toast" id="global-toast"></div>

        <!-- Movement Picker Modal -->
        <div class="modal-overlay" id="mv-picker-overlay" onclick="closeMovementPickerOverlay(event)">"""

assert old_toast_anchor in html, "Toast anchor not found"
html = html.replace(old_toast_anchor, new_toast_anchor, 1)
print("✅ Toast element added")

# ---------------------------------------------------------------
# 6) Replace movement picker JS functions (4064~4226 area)
# ---------------------------------------------------------------
old_picker_js_start = "        // ===== Movement Picker (for course/self linking) ====="
old_picker_js_end = "        function buildMovementSourceLabel(context, record) {"

# Find exact span
idx_start = html.find(old_picker_js_start)
idx_end = html.find(old_picker_js_end, idx_start)
assert idx_start > 0 and idx_end > idx_start, "Picker JS span not found"

new_picker_js = """        // ===== Movement Picker (for course/self linking) =====
        // Current picker context: 'course' or 'self'
        let mvPickerContext = 'course';
        let mvPickerCategory = 'posture';
        let mvPickerSelectedIds = [];
        // Active note index for the current context (so picker knows which note to populate)
        let mvPickerActiveNoteIdx = -1;

        function openMovementPicker(context, noteIdx) {
            mvPickerContext = context;
            mvPickerCategory = 'posture';
            mvPickerSelectedIds = [];
            mvPickerActiveNoteIdx = (typeof noteIdx === 'number') ? noteIdx : -1;

            // Load already linked movements from the target note (if editing a note)
            if (mvPickerActiveNoteIdx >= 0) {
                const notes = getNoteItems(context);
                const target = notes[mvPickerActiveNoteIdx];
                if (target && target.movementIds) {
                    mvPickerSelectedIds = [...target.movementIds];
                }
            }

            document.getElementById('mv-picker-search').value = '';
            document.querySelectorAll('.mv-picker-tab').forEach(t => {
                t.classList.toggle('active', t.dataset.cat === 'posture');
            });
            renderPickerList();
            document.getElementById('mv-picker-overlay').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeMovementPicker() {
            document.getElementById('mv-picker-overlay').classList.remove('active');
            document.body.style.overflow = '';
        }

        function closeMovementPickerOverlay(e) {
            if (e.target === document.getElementById('mv-picker-overlay')) closeMovementPicker();
        }

        function switchPickerTab(cat) {
            mvPickerCategory = cat;
            document.querySelectorAll('.mv-picker-tab').forEach(t => {
                t.classList.toggle('active', t.dataset.cat === cat);
            });
            renderPickerList();
        }

        function filterPickerMovements() {
            renderPickerList();
        }

        function renderPickerList() {
            const lib = getMovementLibrary();
            const search = (document.getElementById('mv-picker-search')?.value || '').toLowerCase().trim();
            const filtered = lib.movements
                .filter(m => m.category === mvPickerCategory)
                .filter(m => {
                    if (!search) return true;
                    return m.nameFr.toLowerCase().includes(search) || m.nameZh.includes(search);
                })
                .sort((a,b) => a.nameFr.localeCompare(b.nameFr, 'fr'));

            const el = document.getElementById('mv-picker-list');
            if (!el) return;

            if (filtered.length === 0) {
                el.innerHTML = '<div class="mv-empty">无匹配动作</div>';
                return;
            }

            el.innerHTML = filtered.map(m => {
                const selected = mvPickerSelectedIds.includes(m.id);
                return `
                <div class="mv-picker-item ${selected ? 'selected' : ''}" onclick="togglePickerSelection('${m.id}')">
                    <div class="info">
                        <div class="fr">${m.nameFr}</div>
                        <div class="zh">${m.nameZh}</div>
                    </div>
                    <div class="check">${selected ? '✓' : ''}</div>
                </div>`;
            }).join('');
        }

        function togglePickerSelection(id) {
            const idx = mvPickerSelectedIds.indexOf(id);
            if (idx >= 0) {
                mvPickerSelectedIds.splice(idx, 1);
            } else {
                mvPickerSelectedIds.push(id);
            }
            renderPickerList();
        }

        // ===== Note Items =====
        // Stored in sessionStorage: noteItems_course, noteItems_self
        // Structure: [{ text: '', movementIds: [] }]
        function getNoteItems(context) {
            const raw = sessionStorage.getItem('noteItems_' + context);
            if (raw) {
                try { return JSON.parse(raw); } catch (e) {}
            }
            return [{ text: '', movementIds: [] }];
        }
        function setNoteItems(context, arr) {
            sessionStorage.setItem('noteItems_' + context, JSON.stringify(arr));
        }
        function addNoteItem(context) {
            const notes = getNoteItems(context);
            notes.push({ text: '', movementIds: [] });
            setNoteItems(context, notes);
            renderNoteItemList(context);
        }
        function removeNoteItem(context, idx) {
            const notes = getNoteItems(context);
            notes.splice(idx, 1);
            // Ensure at least one empty note exists
            if (notes.length === 0) notes.push({ text: '', movementIds: [] });
            setNoteItems(context, notes);
            renderNoteItemList(context);
        }
        function updateNoteText(context, idx, text) {
            const notes = getNoteItems(context);
            if (!notes[idx]) return;
            notes[idx].text = text;
            setNoteItems(context, notes);
            // don't re-render (would break focus)
        }
        function removeNoteMovement(context, noteIdx, mvId) {
            const notes = getNoteItems(context);
            if (!notes[noteIdx]) return;
            notes[noteIdx].movementIds = (notes[noteIdx].movementIds || []).filter(id => id !== mvId);
            setNoteItems(context, notes);
            renderNoteItemList(context);
        }
        function renderNoteItemList(context) {
            const notes = getNoteItems(context);
            const el = document.getElementById(context + '-notes-list');
            if (!el) return;
            const lib = getMovementLibrary();

            el.innerHTML = notes.map((n, i) => {
                const tags = (n.movementIds || []).map(mvId => {
                    const m = lib.movements.find(x => x.id === mvId);
                    const name = m ? m.nameFr : mvId;
                    return `<span class="note-item-tag">${name}<span class="remove" onclick="event.stopPropagation();removeNoteMovement('${context}',${i},'${mvId}')">×</span></span>`;
                }).join('');
                const textEscaped = escapeHtml(n.text || '');
                return `
                <div class="note-item">
                    <textarea rows="3" placeholder="笔记内容..." oninput="updateNoteText('${context}',${i},this.value)">${textEscaped}</textarea>
                    ${tags ? `<div class="note-item-tags">${tags}</div>` : ''}
                    <div class="note-item-actions">
                        <span class="note-item-pick" onclick="openMovementPicker('${context}', ${i})">+ 关联动作</span>
                        <span class="note-item-del" onclick="removeNoteItem('${context}',${i})">删除</span>
                    </div>
                </div>`;
            }).join('');
        }

        // Legacy getLinkedMovements / setLinkedMovements / renderLinkedMovementsTrigger
        // These now operate on ALL movements across all notes (used for detail display / history)
        function getLinkedMovements(context) {
            const notes = getNoteItems(context);
            const ids = new Set();
            notes.forEach(n => (n.movementIds || []).forEach(id => ids.add(id)));
            const lib = getMovementLibrary();
            return Array.from(ids).map(id => {
                const m = lib.movements.find(x => x.id === id);
                return { id, note: '' };
            });
        }
        function setLinkedMovements(context, arr) {
            // Legacy compatibility: replaces all linked movements across notes
            // We assign them to the first note (or create one)
            const notes = getNoteItems(context);
            if (notes.length === 0) notes.push({ text: '', movementIds: [] });
            notes[0].movementIds = arr.map(a => a.id);
            setNoteItems(context, notes);
        }
        function renderLinkedMovementsTrigger(context) {
            // Legacy: no longer a single trigger since each note has its own picker
            // Kept for backward compatibility with reset forms etc.
            renderNoteItemList(context);
        }
        function removeLinkedMovement(context, id) {
            const notes = getNoteItems(context);
            notes.forEach(n => {
                n.movementIds = (n.movementIds || []).filter(mid => mid !== id);
            });
            setNoteItems(context, notes);
            renderNoteItemList(context);
        }

        function confirmMovementPicker() {
            const context = mvPickerContext;
            const noteIdx = mvPickerActiveNoteIdx;
            if (noteIdx >= 0) {
                const notes = getNoteItems(context);
                if (!notes[noteIdx]) {
                    closeMovementPicker();
                    return;
                }
                notes[noteIdx].movementIds = [...mvPickerSelectedIds];
                setNoteItems(context, notes);
                renderNoteItemList(context);
            }
            closeMovementPicker();
        }

        // Sync linked movement key points to movement library (called on save of course/self)
        function syncLinkedKeyPoints(context, record) {
            const notes = getNoteItems(context);
            if (!notes || !notes.length) return 0;
            const lib = getMovementLibrary();
            const sourceLabel = buildMovementSourceLabel(context, record);
            let synced = 0;

            notes.forEach(note => {
                const text = (note.text || '').trim();
                if (!text) return;
                const mids = note.movementIds || [];
                if (!mids.length) return;
                mids.forEach(mvId => {
                    const m = lib.movements.find(x => x.id === mvId);
                    if (!m) return;
                    if (!m.keyPoints) m.keyPoints = [];
                    const dup = m.keyPoints.some(kp => kp.text === text && kp.source === sourceLabel);
                    if (!dup) {
                        m.keyPoints.push({ text, source: sourceLabel });
                        synced++;
                    }
                });
            });
            if (synced > 0) {
                saveMovementLibrary(lib);
            }
            return synced;
        }

        function showToast(msg) {
            const t = document.getElementById('global-toast');
            if (!t) return;
            t.textContent = msg;
            t.classList.add('show');
            clearTimeout(t._timer);
            t._timer = setTimeout(() => t.classList.remove('show'), 1800);
        }

        function escapeHtml(s) {
            return String(s).replace(/[&<>"']/g, c => ({
                '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
            })[c]);
        }

        function buildMovementSourceLabel(context, record) {
"""

# Replace the span
html = html[:idx_start] + new_picker_js + html[idx_end:]
print("✅ Movement picker + note item JS replaced")

# ---------------------------------------------------------------
# 7) Update resetCourseForm: remove textarea reset, add note item reset
# ---------------------------------------------------------------
old_reset_course = """            document.getElementById('course-notes').value = '';
            savePhotos('course', []); savePhotos('course-notes', []);
            renderPhotoPreview('course'); renderPhotoPreview('course-notes');
            updateDifficultyVisibility();
            setLinkedMovements('course', []);
            renderLinkedMovementsTrigger('course');"""

new_reset_course = """            setNoteItems('course', [{ text: '', movementIds: [] }]);
            renderNoteItemList('course');
            savePhotos('course', []); savePhotos('course-notes', []);
            renderPhotoPreview('course'); renderPhotoPreview('course-notes');
            updateDifficultyVisibility();"""

assert old_reset_course in html, "resetCourseForm block not found"
html = html.replace(old_reset_course, new_reset_course, 1)
print("✅ resetCourseForm updated")

# ---------------------------------------------------------------
# 8) Update resetSelfForm
# ---------------------------------------------------------------
old_reset_self = """            document.getElementById('self-notes').value = '';
            savePhotos('self', []); savePhotos('self-notes', []);
            renderPhotoPreview('self'); renderPhotoPreview('self-notes');
            setLinkedMovements('self', []);
            renderLinkedMovementsTrigger('self');"""

new_reset_self = """            setNoteItems('self', [{ text: '', movementIds: [] }]);
            renderNoteItemList('self');
            savePhotos('self', []); savePhotos('self-notes', []);
            renderPhotoPreview('self'); renderPhotoPreview('self-notes');"""

assert old_reset_self in html, "resetSelfForm block not found"
html = html.replace(old_reset_self, new_reset_self, 1)
print("✅ resetSelfForm updated")

# ---------------------------------------------------------------
# 9) Update addCoursePlan: notes field + sync with toast
# ---------------------------------------------------------------
old_course_save = """                notes: document.getElementById('course-notes').value,
                notePhotos: getPhotos('course-notes'),
                linkedMovements: getLinkedMovements('course')
            };
            if (editState.module === 'coursePlans' && editState.index >= 0) {
                data[editState.index] = record;
            } else {
                data.push(record);
            }
            saveData('coursePlans', data);
            savePhotos('course', []); savePhotos('course-notes', []);
            syncCourseToExpenses();
            syncLinkedKeyPoints('course', record);
            setLinkedMovements('course', []);
            renderLinkedMovementsTrigger('course');"""

new_course_save = """                notes: getNoteItems('course'),
                notePhotos: getPhotos('course-notes')
            };
            if (editState.module === 'coursePlans' && editState.index >= 0) {
                data[editState.index] = record;
            } else {
                data.push(record);
            }
            saveData('coursePlans', data);
            savePhotos('course', []); savePhotos('course-notes', []);
            syncCourseToExpenses();
            const syncedCount = syncLinkedKeyPoints('course', record);
            if (syncedCount > 0) showToast('已同步' + syncedCount + '条要点到动作库');
            setNoteItems('course', [{ text: '', movementIds: [] }]);
            renderNoteItemList('course');"""

assert old_course_save in html, "Course save block not found"
html = html.replace(old_course_save, new_course_save, 1)
print("✅ addCoursePlan updated")

# ---------------------------------------------------------------
# 10) Update addSelfTraining
# ---------------------------------------------------------------
old_self_save = """                notes: document.getElementById('self-notes').value,
                notePhotos: getPhotos('self-notes'),
                linkedMovements: getLinkedMovements('self')
            };
            if (editState.module === 'selfTrainingPlans' && editState.index >= 0) {
                data[editState.index] = record;
            } else {
                data.push(record);
            }
            saveData('selfTrainingPlans', data);
            savePhotos('self', []); savePhotos('self-notes', []);
            syncLinkedKeyPoints('self', record);
            setLinkedMovements('self', []);
            renderLinkedMovementsTrigger('self');"""

new_self_save = """                notes: getNoteItems('self'),
                notePhotos: getPhotos('self-notes')
            };
            if (editState.module === 'selfTrainingPlans' && editState.index >= 0) {
                data[editState.index] = record;
            } else {
                data.push(record);
            }
            saveData('selfTrainingPlans', data);
            savePhotos('self', []); savePhotos('self-notes', []);
            const syncedCount = syncLinkedKeyPoints('self', record);
            if (syncedCount > 0) showToast('已同步' + syncedCount + '条要点到动作库');
            setNoteItems('self', [{ text: '', movementIds: [] }]);
            renderNoteItemList('self');"""

assert old_self_save in html, "Self save block not found"
html = html.replace(old_self_save, new_self_save, 1)
print("✅ addSelfTraining updated")

# ---------------------------------------------------------------
# 11) Update editCoursePlan: load notes array into form
# ---------------------------------------------------------------
old_course_edit_notes = """            document.getElementById('course-notes').value = d.notes || '';
            if (d.photos?.length) { savePhotos('course', [...d.photos]); renderPhotoPreview('course'); }
            else { savePhotos('course', []); renderPhotoPreview('course'); }
            if (d.notePhotos?.length) { savePhotos('course-notes', [...d.notePhotos]); renderPhotoPreview('course-notes'); }
            else { savePhotos('course-notes', []); renderPhotoPreview('course-notes'); }
            if (d.linkedMovements?.length) { setLinkedMovements('course', [...d.linkedMovements]); renderLinkedMovementsTrigger('course'); }
            else { setLinkedMovements('course', []); renderLinkedMovementsTrigger('course'); }"""

new_course_edit_notes = """            const courseNotes = normalizeNotes(d.notes);
            setNoteItems('course', courseNotes);
            renderNoteItemList('course');
            if (d.photos?.length) { savePhotos('course', [...d.photos]); renderPhotoPreview('course'); }
            else { savePhotos('course', []); renderPhotoPreview('course'); }
            if (d.notePhotos?.length) { savePhotos('course-notes', [...d.notePhotos]); renderPhotoPreview('course-notes'); }
            else { savePhotos('course-notes', []); renderPhotoPreview('course-notes'); }"""

assert old_course_edit_notes in html, "Course edit notes block not found"
html = html.replace(old_course_edit_notes, new_course_edit_notes, 1)
print("✅ editCoursePlan notes updated")

# ---------------------------------------------------------------
# 12) Update editSelfTraining: load notes array into form
# ---------------------------------------------------------------
old_self_edit_notes = """            document.getElementById('self-notes').value = d.notes || '';
            if (d.photos?.length) { savePhotos('self', [...d.photos]); renderPhotoPreview('self'); }
            else { savePhotos('self', []); renderPhotoPreview('self'); }
            if (d.notePhotos?.length) { savePhotos('self-notes', [...d.notePhotos]); renderPhotoPreview('self-notes'); }
            else { savePhotos('self-notes', []); renderPhotoPreview('self-notes'); }
            if (d.linkedMovements?.length) { setLinkedMovements('self', [...d.linkedMovements]); renderLinkedMovementsTrigger('self'); }
            else { setLinkedMovements('self', []); renderLinkedMovementsTrigger('self'); }"""

new_self_edit_notes = """            const selfNotes = normalizeNotes(d.notes);
            setNoteItems('self', selfNotes);
            renderNoteItemList('self');
            if (d.photos?.length) { savePhotos('self', [...d.photos]); renderPhotoPreview('self'); }
            else { savePhotos('self', []); renderPhotoPreview('self'); }
            if (d.notePhotos?.length) { savePhotos('self-notes', [...d.notePhotos]); renderPhotoPreview('self-notes'); }
            else { savePhotos('self-notes', []); renderPhotoPreview('self-notes'); }"""

assert old_self_edit_notes in html, "Self edit notes block not found"
html = html.replace(old_self_edit_notes, new_self_edit_notes, 1)
print("✅ editSelfTraining notes updated")

# ---------------------------------------------------------------
# 13) Add normalizeNotes helper + notes display for calendar/detail
#     Find a good insertion point - right after buildMovementSourceLabel
# ---------------------------------------------------------------
# First, find end of buildMovementSourceLabel
old_bmsl = """        function buildMovementSourceLabel(context, record) {
            const date = record.date || today;
            if (context === 'course') {
                const inst = record.institution ? record.institution + ' ' : '';
                const type = record.courseType || '';
                return `来自${inst}${type}课程 / ${date}`;
            } else {
                const loc = record.location || '';
                const type = record.selfType || record.trainingType || '';
                return `来自自训${type ? '·' + type : ''} / ${date}`;
            }
        }"""

new_bmsl = old_bmsl + """

        // Normalize legacy plain-text notes or old linkedMovements to new notes array format
        function normalizeNotes(notesField) {
            if (Array.isArray(notesField) && notesField.length > 0) {
                // Ensure each item has movementIds
                return notesField.map(n => ({
                    text: n.text || '',
                    movementIds: Array.isArray(n.movementIds) ? n.movementIds : []
                }));
            }
            if (typeof notesField === 'string' && notesField.trim()) {
                return [{ text: notesField, movementIds: [] }];
            }
            return [{ text: '', movementIds: [] }];
        }

        // Get a flat text preview (first non-empty note) for list display
        function getNotesPreview(notesField, maxLen) {
            maxLen = maxLen || 50;
            if (Array.isArray(notesField)) {
                const firstText = notesField.find(n => n.text && n.text.trim());
                return firstText ? firstText.text.substring(0, maxLen) + (firstText.text.length > maxLen ? '...' : '') : '';
            }
            if (typeof notesField === 'string' && notesField.trim()) {
                return notesField.substring(0, maxLen) + (notesField.length > maxLen ? '...' : '');
            }
            return '';
        }

        // Render notes array as HTML for detail views (card body)
        function renderNotesDetailHtml(notesField) {
            const lib = getMovementLibrary();
            if (Array.isArray(notesField) && notesField.length > 0) {
                return notesField.map(n => {
                    const text = escapeHtml(n.text || '');
                    if (!text && (!n.movementIds || !n.movementIds.length)) return '';
                    let tags = '';
                    if (n.movementIds && n.movementIds.length) {
                        tags = '<div class="note-item-tags">';
                        n.movementIds.forEach(mvId => {
                            const m = lib.movements.find(x => x.id === mvId);
                            const name = m ? m.nameFr : mvId;
                            tags += '<span class="note-item-tag">' + name + '</span>';
                        });
                        tags += '</div>';
                    }
                    return '<div class="note-item">' + (text ? '<div style="font-size:13px;color:var(--text-primary);white-space:pre-wrap;">' + text + '</div>' : '') + tags + '</div>';
                }).filter(Boolean).join('');
            }
            // Legacy plain text
            if (typeof notesField === 'string' && notesField.trim()) {
                return '<div class="note-item"><div style="font-size:13px;color:var(--text-primary);white-space:pre-wrap;">' + escapeHtml(notesField) + '</div></div>';
            }
            return '';
        }"""

assert old_bmsl in html, "buildMovementSourceLabel not found"
html = html.replace(old_bmsl, new_bmsl, 1)
print("✅ normalizeNotes + renderNotesDetailHtml helpers added")

# ---------------------------------------------------------------
# 14) Update calendar timeline noteHtml to handle array notes
# ---------------------------------------------------------------
old_cal_note = "                    let noteHtml = r.notes ? '<div class=\"training-list-note\">'+r.notes.substring(0,50)+(r.notes.length>50?'...':'')+'</div>' : '';"
new_cal_note = "                    const notePreview = getNotesPreview(r.notes, 50);\n                    let noteHtml = notePreview ? '<div class=\"training-list-note\">'+notePreview+'</div>' : '';"

assert old_cal_note in html, "Calendar note preview not found"
html = html.replace(old_cal_note, new_cal_note, 1)
print("✅ Calendar timeline note preview updated")

# ---------------------------------------------------------------
# 15) Init: render note item lists when page loads
#     Find the init section and add note list rendering
# ---------------------------------------------------------------
# We'll add initialization at the end of initApp or similar.
# Find a reliable init point.
old_init_anchor = "        function renderAll() {"
new_init_anchor = """        function initNoteForms() {
            setNoteItems('course', [{ text: '', movementIds: [] }]);
            setNoteItems('self', [{ text: '', movementIds: [] }]);
            renderNoteItemList('course');
            renderNoteItemList('self');
        }

        function renderAll() {"""

assert old_init_anchor in html, "renderAll not found"
html = html.replace(old_init_anchor, new_init_anchor, 1)
print("✅ initNoteForms added")

# Find window.onload / DOMContentLoaded or similar init call
old_onload_call = "            renderAll();"
# find first occurrence after initNoteForms definition
idx_onload = html.find(old_onload_call, html.find("initNoteForms"))
if idx_onload > 0:
    # Add initNoteForms call before renderAll
    before = html[:idx_onload]
    after = html[idx_onload + len(old_onload_call):]
    html = before + "            initNoteForms();\n" + old_onload_call + after
    print("✅ initNoteForms() call added to init")
else:
    print("⚠️  renderAll call not found for init injection")

# ---------------------------------------------------------------
# Write back
# ---------------------------------------------------------------
with open(SRC, "w", encoding="utf-8") as f:
    f.write(html)

print("\n🎉 All changes applied successfully!")
print(f"Output file: {SRC}")
print(f"File size: {len(html)} bytes")
