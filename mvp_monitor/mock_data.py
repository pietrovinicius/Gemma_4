def get_mock_patients():
    return [
        {
            "id": 1,
            "nome": "João Silva",
            "idade": 65,
            "setor": "CTI Geral",
            "leito": "Leito 01",
            "status_anterior": "Piora",
            "dados_d1": {
                "medica": "Paciente em choque séptico. Iniciado protocolo. Glasgow 11.",
                "enfermagem": "PA 90x50 mmHg, FC 110, Temp 38.5C. Diurese 400ml/24h.",
                "prescricao": "Noradrenalina 0.5 mcg/kg/min, Fentanil, Ceftriaxona. VNI."
            },
            "dados_d0": {
                "medica": "Melhora do padrão respiratório e hemodinâmico. Desmame de DVA iniciado. Glasgow 14.",
                "enfermagem": "PA 110x70 mmHg, FC 88, Temp 37.1C. Diurese 1200ml/24h.",
                "prescricao": "Noradrenalina 0.1 mcg/kg/min, Fentanil reduzido. Cateter nasal O2 2L/min."
            }
        },
        {
            "id": 2,
            "nome": "Maria Souza",
            "idade": 72,
            "setor": "CTI Cardiológica",
            "leito": "Leito 04",
            "status_anterior": "Melhora",
            "dados_d1": {
                "medica": "Pós-operatório de revascularização. Despertar programado. Glasgow 10.",
                "enfermagem": "PA 100x60 mmHg, FC 90, Temp 36.8C. Tubo orotraqueal.",
                "prescricao": "Fentanil contínuo. Desmame finalizado."
            },
            "dados_d0": {
                "medica": "Extubada hoje cedo. Agitação psicomotora leve, dor retroesternal leve. Glasgow 14.",
                "enfermagem": "PA 105x65 mmHg, FC 95, Temp 37.0C. Dreno mantido.",
                "prescricao": "Morfina SN. Dipirona."
            }
        },
        {
            "id": 3,
            "nome": "Carlos Mendes",
            "idade": 50,
            "setor": "CTI Geral",
            "leito": "Leito 05",
            "status_anterior": "Estagnado",
            "dados_d1": {
                "medica": "Pneumonia grave. Instabilidade hemodinâmica severa. Glasgow 8.",
                "enfermagem": "PA 85x45 mmHg, FC 115, Temp 39.0C. Ventilação mecânica.",
                "prescricao": "Noradrenalina 0.8 mcg/kg/min, Vasopressina 0.04 U/min. Sedação profunda."
            },
            "dados_d0": {
                "medica": "Mantém extrema gravidade, febre persistente, piora radiológica.",
                "enfermagem": "PA 80x40 mmHg, FC 120, Temp 39.2C. Oligúria (O200ml/24h).",
                "prescricao": "Noradrenalina 1.0 mcg/kg/min, Vasopressina mantida. Ajuste de ATB."
            }
        }
    ]

def get_sectors():
    return ["CTI Geral", "CTI Cardiológica", "Unidade Intermediária"]

def get_patients_by_sector(sector):
    return [p for p in get_mock_patients() if p['setor'] == sector]

def get_patient_by_id(patient_id):
    for p in get_mock_patients():
        if p['id'] == patient_id:
            return p
    return None
