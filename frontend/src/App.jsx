import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, ClipboardList, MessageSquare, Loader2, Sparkles, Send, Download, Mic, FileText, Edit3, Settings, Eye, X } from 'lucide-react';
import './index.css';

export default function App() {
  const [step, setStep] = useState(1);
  const [formatos, setFormatos] = useState([]);
  const [demandas, setDemandas] = useState([]);
  const [estado, setEstado] = useState({
    idea: '', formato: '', metodologia: '',
    facultad: '', grupo: '', investigador: '', id_investigador: '',
    sector_tematico: '', arbol_problemas: '', arbol_objetivos: '',
    id_demanda: '', contexto_adicional: '',
    datos_completos: null, expansion_actual: ''
  });
  
  // States
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [clarificacionPregunta, setClarificacionPregunta] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [genSteps, setGenSteps] = useState([false, false, false]);
  
  // Advanced Features State
  const [isRecording, setIsRecording] = useState(false);
  const [isRefining, setIsRefining] = useState(false);
  const [manualMode, setManualMode] = useState(false);
  const [manualSections, setManualSections] = useState([]);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    fetch('/formatos').then(r => r.json()).then(d => setFormatos(d.formatos || [])).catch(() => {});
    fetch('/demands').then(r => r.json()).then(d => setDemandas(d.demandas || [])).catch(() => {});
  }, []);

  const handleChange = (e) => setEstado({ ...estado, [e.target.name]: e.target.value });

  // 1. Dictado por voz - MediaRecorder + Backend
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
        ? 'audio/webm;codecs=opus' 
        : MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg';
      
      const recorder = new MediaRecorder(stream, { mimeType });
      const chunks = [];
      recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };
      
      recorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        const audioBlob = new Blob(chunks, { type: mimeType });
        setIsRefining(true);
        try {
          const formData = new FormData();
          formData.append('file', audioBlob, 'audio.webm');
          const res = await fetch('/transcribir-audio', { method: 'POST', body: formData });
          const text = await res.text();
          if (!text || !text.trim()) { alert('El servidor no respondió. Verifica el backend.'); return; }
          const d = JSON.parse(text);
          if (d.transcripcion) setEstado(prev => ({ ...prev, idea: (prev.idea ? prev.idea + ' ' : '') + d.transcripcion }));
          else if (d.error) alert('Error en transcripción: ' + d.error);
        } catch(err) { alert('Error: ' + err.message); }
        finally { setIsRefining(false); }
      };
      
      recorder.start();
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
      setTimeout(() => stopRecording(), 60000); // Auto-stop 60s
    } catch(err) { alert('Error micrófono: ' + err.message); }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
    }
    setIsRecording(false);
  };

  // 2. Transcription to Idea
  const pasteTranscription = async () => {
    const t = prompt("Pega tu transcripción aquí:");
    if (!t) return;
    setIsRefining(true);
    try {
      const res = await fetch('/transcription-to-idea', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcripcion: t })
      });
      const d = await res.json();
      const txt = d.datos_extraidos?.titulo_proyecto ? `Título: ${d.datos_extraidos.titulo_proyecto}\n${d.datos_extraidos.resumen || ''}` : t;
      setEstado(prev => ({ ...prev, idea: txt }));
    } finally { setIsRefining(false); }
  };

  // 3. AI Refine
  const aiAssist = async () => {
    if (!estado.idea.trim()) return alert("Escribe una idea base primero.");
    setIsRefining(true);
    try {
      const res = await fetch('/refinar-texto', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: estado.idea, objetivo: "profesionalizar académicamente" })
      });
      const d = await res.json();
      if (d.texto_refinado) setEstado(prev => ({ ...prev, idea: d.texto_refinado }));
    } finally { setIsRefining(false); }
  };

  const evaluarIdea = async () => {
    const required = ['idea', 'formato', 'metodologia', 'facultad', 'grupo', 'investigador', 'sector_tematico'];
    const missing = required.filter(f => !estado[f]);
    if (missing.length > 0) return alert('Campos obligatorios (*)');

    setIsEvaluating(true);
    try {
      const res = await fetch('/evaluar', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea: estado.idea, formato: estado.formato })
      });
      const data = await res.json();
      if (!data.lista_para_expandir && data.pregunta) {
        setClarificacionPregunta(data.pregunta); setStep(2);
      } else {
        generarDocumento();
      }
    } catch { alert('Error de red.'); }
    finally { setIsEvaluating(false); }
  };

  const generarDocumento = async () => {
    setStep(3); setIsGenerating(true); setGenSteps([false, false, false]);
    let t = 0;
    const interval = setInterval(() => {
      setGenSteps(p => { const n = [...p]; n[t] = true; return n; });
      t++; if (t >= 3) clearInterval(interval);
    }, 6000);

    try {
      const payload = { ...estado };
      if (step === 2) payload.contexto_adicional = estado.contexto_adicional;
      const res = await fetch('/generar-documento', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.error);

      setEstado(p => ({ ...p, datos_completos: data, expansion_actual: data.texto_previsualizacion || '' }));
      clearInterval(interval); setGenSteps([true, true, true]);
      setTimeout(() => setStep(4), 1000);
    } catch (e) { alert('Error IA: ' + e.message); }
    finally { setIsGenerating(false); }
  };

  // 5. Manual Section Editor Splitter
  const loadManualMode = () => {
    const text = (estado.expansion_actual || '').replace(/```markdown/g, '').replace(/```/g, '');
    if (!text.includes("### ")) return alert("Formato incompatible con editor en bloques.");
    const sections = text.split("### ").filter(s => s.trim() !== "");
    const parsed = sections.map(sec => {
      const lines = sec.trim().split("\n");
      const title = lines.shift() || "Sección";
      return { title, content: lines.join("\n").trim() };
    });
    setManualSections(parsed);
    setManualMode(true);
  };

  const saveManualMode = () => {
    const newMarkdown = manualSections.map(s => `### ${s.title}\n${s.content}\n\n`).join('');
    setEstado(p => ({ ...p, expansion_actual: newMarkdown.trim() }));
    setManualMode(false);
  };

  const updateSectionInfo = (index, value) => {
    const next = [...manualSections];
    next[index].content = value;
    setManualSections(next);
  };

  const generarPdfFinal = async () => {
    try {
      const payload = {
        ...estado.datos_completos.datos_expansion,
        equipo: estado.datos_completos.equipo,
        match_evaluacion: estado.datos_completos.match_evaluacion,
        expansion: estado.expansion_actual || estado.datos_completos.texto_previsualizacion,
        idea_original: estado.idea,
        formato_nombre: estado.datos_completos.formato_nombre
      };
      const res = await fetch('/generar-pdf-final', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.pdf_url) {
        const pdfRes = await fetch(data.pdf_url);
        const blob = await pdfRes.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename || 'propuesta_nexus.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else alert('Error: ' + data.error);
    } catch { alert('Generando Error VPN o PDF'); }
  };

  const RenderMarkdown = ({ markdown }) => {
    let html = (markdown || '')
      .replace(/```markdown/g, '').replace(/```/g, '')
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/^\- (.*$)/gim, '<li>$1</li>')
      .replace(/\n\n/g, '<p></p>').replace(/\n/g, '<br/>');
    return <div className="markdown-preview" dangerouslySetInnerHTML={{ __html: html }} />;
  };

  return (
    <div className="app-container">
      <header className="glass-panel" style={{ borderRadius: 0, margin: 0 }}>
        <div className="logo-wrap">
          <div className="logo-icon">N</div>
          <div className="logo-text"><strong>Project Nexus</strong><span>Motor React</span></div>
        </div>
        <div className="badge-version">v1.0 (Premium)</div>
      </header>

      <section className="hero">
        <div className="hero-tag"><Sparkles size={14} /> UI Revolucionada</div>
        <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          Transforma tu idea en una <em>Propuesta Élite</em>
        </motion.h1>
      </section>

      <main>
        <div className="steps-bar">
          {['Proyecto', 'Clarificación', 'Formulación', 'Revisión'].map((name, i) => (
             <div key={i} className={`step-item ${step === i + 1 ? 'active' : ''} ${step > i + 1 ? 'completed' : ''}`}>
               <div className="step-icon-wrap">{i + 1}</div>
               <div className="step-title">{name}</div>
             </div>
          ))}
        </div>

        <AnimatePresence mode='wait'>
          {step === 1 && (
            <motion.div key="p1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="glass-panel form-panel">
              <div className="panel-header">
                <div className="panel-icon-box"><ClipboardList size={26} /></div>
                <div className="panel-header-text"><h2>Formulario Técnico</h2></div>
              </div>

              <div className="section-label">A. Concepto de Innovación</div>
              <div className="input-group">
                <div className="input-label" style={{display:'flex', justifyContent:'space-between'}}>
                   Idea Semilla <span className="req">*</span>
                   <button className="btn-outline" onClick={aiAssist} disabled={isRefining} style={{padding:'4px 10px', fontSize:11, borderRadius:6}}>
                      {isRefining ? <Loader2 className="spinner" size={14} style={{borderTopColor:'transparent',width:14,height:14}}/> : <Sparkles size={14} />} Refinar IA
                   </button>
                </div>
                <div style={{position:'relative'}}>
                   <textarea className="input-field" name="idea" value={estado.idea} onChange={handleChange} placeholder="Describe qué, para quién..."></textarea>

                </div>
              </div>

              <div className="grid-2">
                 <div className="input-group">
                    <div className="input-label">Sector <span className="req">*</span></div>
                    <select className="input-field" name="sector_tematico" value={estado.sector_tematico} onChange={handleChange}>
                       <option value="">— Selecciona —</option>
                       <option>Salud y Bienestar</option>
                       <option>Transición Energética</option>
                       <option>Tecnologías de la Información (TIC)</option>
                       <option>Agroindustria y Seguridad Alimentaria</option>
                       <option>Educación de Calidad</option>
                       <option>Medio Ambiente y Cambio Climático</option>
                       <option>Desarrollo Social y Comunitario</option>
                       <option>Biotecnología y Ciencias de la Vida</option>
                       <option>Ingeniería y Manufactura Avanzada</option>
                       <option>Economía Circular y Sostenibilidad</option>
                       <option>Desarrollo Urbano y Smart Cities</option>
                       <option>Cultura, Artes y Economía Naranja</option>
                       <option>Ciberseguridad y Blockchain</option>
                    </select>
                 </div>
                 <div className="input-group">
                    <div className="input-label">Formato <span className="req">*</span></div>
                    <select className="input-field" name="formato" value={estado.formato} onChange={handleChange}>
                       <option value="">— Selecciona —</option>
                       {formatos.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
                    </select>
                 </div>
              </div>

              <div className="section-label">B. Identificación</div>
              <div className="grid-2">
                 <div className="input-group"><div className="input-label">Investigador (PI) <span className="req">*</span></div><input type="text" className="input-field" name="investigador" value={estado.investigador} onChange={handleChange} /></div>
                 <div className="input-group"><div className="input-label">Facultad <span className="req">*</span></div><input type="text" className="input-field" name="facultad" value={estado.facultad} onChange={handleChange} /></div>
                 <div className="input-group">
                     <div className="input-label">Metodología Propuesta <span className="req">*</span></div>
                     <select className="input-field" name="metodologia" value={estado.metodologia} onChange={handleChange}>
                        <option value="">— Selecciona —</option>
                        <option value="Marco Lógico">MGA / Marco Lógico (DNP Colombia)</option>
                        <option value="Erasmus+ Guide">Pautas Erasmus+ KA220</option>
                        <option value="Design Thinking">Design Thinking / UX Research</option>
                        <option value="Agile" >Agile / Scrum for Research</option>
                        <option value="Investigación-Acción">Investigación-Acción Participativa</option>
                     </select>
                 </div>
                 <div className="input-group"><div className="input-label">Grupo de Investigación <span className="req">*</span></div><input type="text" className="input-field" name="grupo" value={estado.grupo} onChange={handleChange} /></div>
              </div>

              <div className="panel-actions">
                 <button className="btn btn-primary" onClick={evaluarIdea} disabled={isEvaluating}>
                    {isEvaluating ? <Loader2 className="spinner" style={{width:20, height:20, margin:0, borderTopColor:'transparent'}} size={20} /> : <Send size={18} />} Formular
                 </button>
              </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="p2" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-panel form-panel">
               <div className="panel-header"><div className="panel-icon-box"><MessageSquare /></div><div className="panel-header-text"><h2>Clarificación</h2></div></div>
               <p style={{marginBottom: '1rem', color: 'var(--azul-med)', fontWeight: 600}}>{clarificacionPregunta}</p>
               <textarea className="input-field" name="contexto_adicional" onChange={handleChange}></textarea>
               <div className="panel-actions">
                 <button className="btn btn-outline" onClick={generarDocumento}>Omitir</button>
                 <button className="btn btn-primary" onClick={generarDocumento}>Continuar</button>
               </div>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div key="p3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-panel form-panel text-center">
               <div className="loading-box">
                 <Loader2 className="spinner" style={{width:50, height:50, margin:'0 auto 1.5rem', borderTopColor:'transparent'}} size={50} />
                 <h2>Nexus procesando...</h2>
                 <div style={{display:'flex', flexDirection:'column', gap:'10px', alignItems:'center', marginTop:15}}>
                    {['Expansión Retórica', 'Asignación Talento', 'Consolidando Módulos'].map((s, i) => (
                       <div key={i} style={{opacity: genSteps[i] ? 1 : 0.4, transition: '0.5s', fontWeight: 600}}>
                          {genSteps[i] && <span style={{color:'var(--verde)', marginRight:8}}>✓</span>} {s}
                       </div>
                    ))}
                 </div>
               </div>
            </motion.div>
          )}

          {step === 4 && (
            <motion.div key="p4" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="glass-panel form-panel">
               <div className="panel-header">
                  <div className="panel-icon-box"><Sparkles /></div>
                  <div className="panel-header-text"><h2>Revisión Élite</h2></div>
               </div>
               
               <div style={{textAlign:'center', padding:'2.5rem 1rem', background:'var(--fondo)', borderRadius:'12px', border:'1px solid var(--linea)', marginBottom:'2rem'}}>
                  <h3 style={{color:'var(--azul)', marginBottom:'0.5rem', fontFamily:'Playfair Display, serif', fontSize:'1.8rem'}}>¡Documento Formulado Exitosamente!</h3>
                  <p style={{color:'var(--suave)', marginBottom:'1.5rem'}}>La IA ha generado una propuesta estructurada de aproximadamente {estado.expansion_actual?.split(' ').length || 0} palabras.</p>
                  
                  <button className="btn btn-primary" onClick={() => setShowPreviewModal(true)} style={{fontSize:'16px', padding:'14px 32px'}}>
                     <Eye size={20} /> Ver Vista Previa del Documento
                  </button>
               </div>
               
               <div style={{marginTop:'2rem', display:'flex', gap:'1rem'}}>
                  <button className="btn btn-outline" onClick={loadManualMode} style={{flex:1}}><Edit3 size={18}/> Edición por Bloques</button>
               </div>

                <div className="panel-actions center" style={{marginTop:'3rem', gap:'1rem'}}>
                   <button className="btn btn-accent" onClick={generarPdfFinal}>
                      <Download size={18} /> Generar y Descargar PDF Técnico
                   </button>
                   <button className="btn btn-outline" onClick={() => {
                     setStep(1);
                     setEstado({ idea: '', formato: '', metodologia: '', facultad: '', grupo: '', investigador: '', id_investigador: '', sector_tematico: '', arbol_problemas: '', arbol_objetivos: '', id_demanda: '', contexto_adicional: '', datos_completos: null, expansion_actual: '' });
                     setClarificacionPregunta('');
                     setGenSteps([false, false, false]);
                     setManualSections([]);
                     setManualMode(false);
                     setShowPreviewModal(false);
                   }}>
                      <ClipboardList size={18} /> Nuevo Proyecto
                   </button>
                </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* ── Modal de Vista Previa ── */}
      <AnimatePresence>
        {showPreviewModal && (
          <motion.div className="modal-overlay" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}>
            <motion.div className="modal-content" initial={{scale:0.95, opacity:0}} animate={{scale:1, opacity:1}} exit={{scale:0.95, opacity:0}} transition={{type:'spring', stiffness:300, damping:25}}>
               <div className="modal-header">
                 <h3>Borrador de Propuesta Generado</h3>
                 <button className="modal-close" onClick={() => setShowPreviewModal(false)}><X size={26}/></button>
               </div>
               <div className="modal-body">
                 <RenderMarkdown markdown={estado.expansion_actual} />
               </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Modal de Edición por Bloques ── */}
      <AnimatePresence>
        {manualMode && (
          <motion.div className="modal-overlay" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}>
            <motion.div className="modal-content" initial={{scale:0.95, opacity:0}} animate={{scale:1, opacity:1}} exit={{scale:0.95, opacity:0}} transition={{type:'spring', stiffness:300, damping:25}}>
               <div className="modal-header">
                 <h3>Edición Manual Avanzada</h3>
                 <button className="modal-close" onClick={() => setManualMode(false)}><X size={26}/></button>
               </div>
               <div className="modal-body" style={{background:'#f1f5f9'}}>
                 {manualSections.map((sec, i) => (
                   <div key={i} style={{marginBottom: '1.5rem', border:'1px solid var(--linea)', padding:'1.5rem', borderRadius:'12px', background:'var(--blanco)', boxShadow:'var(--shadow-sm)'}}>
                      <h3 style={{color:'var(--azul-med)', marginBottom:'0.8rem', fontSize:'1.1rem'}}>{sec.title.replace(/[*#]/g, '')}</h3>
                      <textarea className="input-field" value={sec.content} onChange={e => updateSectionInfo(i, e.target.value)} style={{fontFamily:'monospace', minHeight:180, fontSize:'14px'}}></textarea>
                   </div>
                 ))}
               </div>
               <div className="modal-footer">
                 <button className="btn btn-outline" onClick={() => setManualMode(false)}>Descartar Cambios</button>
                 <button className="btn btn-primary" onClick={saveManualMode}><Download size={16} /> Guardar Documento Editado</button>
               </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
