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
                "prescricao": "Noradrenalina 0.5 mcg/kg/min, Fentanil, Ceftriaxona. VNI.",
                "sinais_vitais": {"pa": "90x50", "fc": 110, "temp": 38.5, "spo2": 90, "diurese": 400}
            },
            "dados_d0": {
                "medica": "Melhora do padrão respiratório e hemodinâmico. Desmame de DVA iniciado. Glasgow 14.",
                "enfermagem": "PA 110x70 mmHg, FC 88, Temp 37.1C. Diurese 1200ml/24h.",
                "prescricao": "Noradrenalina 0.1 mcg/kg/min, Fentanil reduzido. Cateter nasal O2 2L/min.",
                "sinais_vitais": {"pa": "110x70", "fc": 88, "temp": 37.1, "spo2": 95, "diurese": 1200}
            }
        },
        {
            "id": 2,
            "nome": "Maria Souza",
            "idade": 72,
            "setor": "UCO",
            "leito": "Leito 08",
            "status_anterior": "Melhora",
            "dados_d1": {
                "medica": "Pós-operatório de revascularização. Despertar programado. Glasgow 10.",
                "enfermagem": "PA 100x60 mmHg, FC 90, Temp 36.8C. Tubo orotraqueal.",
                "prescricao": "Fentanil contínuo. Desmame finalizado.",
                "sinais_vitais": {"pa": "100x60", "fc": 90, "temp": 36.8, "spo2": 98, "diurese": 800}
            },
            "dados_d0": {
                "medica": "Extubada hoje cedo. Agitação psicomotora leve, dor retroesternal leve. Glasgow 14.",
                "enfermagem": "PA 105x65 mmHg, FC 95, Temp 37.0C. Dreno mantido.",
                "prescricao": "Morfina SN. Dipirona.",
                "sinais_vitais": {"pa": "105x65", "fc": 95, "temp": 37.0, "spo2": 97, "diurese": 1000}
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
                "prescricao": "Noradrenalina 0.8 mcg/kg/min, Vasopressina 0.04 U/min. Sedação profunda.",
                "sinais_vitais": {"pa": "85x45", "fc": 115, "temp": 39.0, "spo2": 88, "diurese": 300}
            },
            "dados_d0": {
                "medica": "Mantém extrema gravidade, febre persistente, piora radiológica.",
                "enfermagem": "PA 80x40 mmHg, FC 120, Temp 39.2C. Oligúria (O200ml/24h).",
                "prescricao": "Noradrenalina 1.0 mcg/kg/min, Vasopressina mantida. Ajuste de ATB.",
                "sinais_vitais": {"pa": "80x40", "fc": 120, "temp": 39.2, "spo2": 85, "diurese": 200}
            }
        },
        {
            "id": 4,
            "nome": "Mariana Souza",
            "idade": 58,
            "setor": "UCO",
            "leito": "Leito 02",
            "status_anterior": "Melhora",
            "dados_d1": {
                "medica": "Pós-op de cirurgia cardíaca (Troca Valvar). Hemodinâmica dependente de DVA média. Glasgow 11.",
                "enfermagem": "PA 95x55 mmHg, FC 88, Temp 36.5C. Sangramento pelo dreno 200ml.",
                "prescricao": "Noradrenalina 0.3 mcg/kg/min, Dobutamina 5 mcg/kg/min.",
                "sinais_vitais": {"pa": "95x55", "fc": 88, "temp": 36.5, "spo2": 96, "diurese": 600}
            },
            "dados_d0": {
                "medica": "Paciente estável, sangramento cessado. DVA em queda progressiva. Glasgow 14.",
                "enfermagem": "PA 110x65 mmHg, FC 80, Temp 36.8C. Dreno seroso 50ml.",
                "prescricao": "Noradrenalina 0.05 mcg/kg/min, Dobutamina suspensa.",
                "sinais_vitais": {"pa": "110x65", "fc": 80, "temp": 36.8, "spo2": 99, "diurese": 1500}
            }
        },
        {
            "id": 5,
            "nome": "Roberto Dias",
            "idade": 48,
            "setor": "CTI Geral",
            "leito": "Leito 03",
            "status_anterior": "Piora",
            "dados_d1": {
                "medica": "Admitido por sepse de foco abdominal. Peritonite. Glasgow 13.",
                "enfermagem": "PA 100x60 mmHg, FC 105, Temp 38.0C. Dreno abdominal com secreção purulenta.",
                "prescricao": "Noradrenalina 0.1 mcg/kg/min, Meropenem.",
                "sinais_vitais": {"pa": "100x60", "fc": 105, "temp": 38.0, "spo2": 94, "diurese": 800}
            },
            "dados_d0": {
                "medica": "Evolui com choque séptico refratário. Pico febril e acidose. Glasgow 9.",
                "enfermagem": "PA 85x45 mmHg, FC 130, Temp 39.5C. Anúrico nas últimas 6h.",
                "prescricao": "Noradrenalina 1.2 mcg/kg/min, Vasopressina 0.04 U/min, IOT e VM.",
                "sinais_vitais": {"pa": "85x45", "fc": 130, "temp": 39.5, "spo2": 89, "diurese": 50}
            }
        },
        {
            "id": 6,
            "nome": "Luciana Lima",
            "idade": 81,
            "setor": "CTI Geral",
            "leito": "Leito 04",
            "status_anterior": "Estagnado",
            "dados_d1": {
                "medica": "Desmame ventilatório difícil pós-trauma torácico. PSV mantido. Glasgow 15.",
                "enfermagem": "PA 120x80 mmHg, FC 75, Temp 36.6C.",
                "prescricao": "Sem DVA. Nutrição Enteral.",
                "sinais_vitais": {"pa": "120x80", "fc": 75, "temp": 36.6, "spo2": 95, "diurese": 1400}
            },
            "dados_d0": {
                "medica": "Mantém desmame ventilatório. Dinâmica respiratória de limite. PSV 10. Estável sem regressão.",
                "enfermagem": "PA 115x75 mmHg, FC 78, Temp 36.7C.",
                "prescricao": "Sem DVA. Nutrição Enteral. Fisioterapia motora.",
                "sinais_vitais": {"pa": "115x75", "fc": 78, "temp": 36.7, "spo2": 95, "diurese": 1500}
            }
        },
        {
            "id": 7,
            "nome": "Fernando Cruz",
            "idade": 69,
            "setor": "CTI Geral",
            "leito": "Leito 06",
            "status_anterior": "Piora",
            "dados_d1": {
                "medica": "DPOC crônico exacerbado. VNI intermitente. Glasgow 14.",
                "enfermagem": "PA 140x90 mmHg, FC 90, Temp 37.0C. Uso de VNI 4/4h.",
                "prescricao": "Hidrocortisona, Broncodilatadores.",
                "sinais_vitais": {"pa": "140x90", "fc": 90, "temp": 37.0, "spo2": 92, "diurese": 1100}
            },
            "dados_d0": {
                "medica": "Rebaixamento sensório e sinais de fadiga muscular. Retenção de CO2 grave. IOT de urgência.",
                "enfermagem": "PA 160x100 mmHg, FC 115, Temp 37.2C. SpO2 84% em uso de máscara não reinalante antes da IOT.",
                "prescricao": "Fentanil, Propofol, Curare para adaptação VM.",
                "sinais_vitais": {"pa": "160x100", "fc": 115, "temp": 37.2, "spo2": 84, "diurese": 800}
            }
        },
        {
            "id": 8,
            "nome": "Beatriz Silva",
            "idade": 34,
            "setor": "UCO",
            "leito": "Leito 07",
            "status_anterior": "Melhora",
            "dados_d1": {
                "medica": "Pós-op de ablação de via acessória (WPW). Sem intercorrências arritmogênicas. Glasgow 15.",
                "enfermagem": "PA 110x70 mmHg, FC 65, Temp 36.5C.",
                "prescricao": "Amiodarona contínua em dose profilática.",
                "sinais_vitais": {"pa": "110x70", "fc": 65, "temp": 36.5, "spo2": 99, "diurese": 1800}
            },
            "dados_d0": {
                "medica": "Holter limpo, estabilidade total. Previsão de alta para o quarto hoje. Glasgow 15.",
                "enfermagem": "PA 115x70 mmHg, FC 70, Temp 36.6C.",
                "prescricao": "Amiodarona suspensa. Medicamento VO apenas.",
                "sinais_vitais": {"pa": "115x70", "fc": 70, "temp": 36.6, "spo2": 99, "diurese": 1600}
            }
        }
    ]

def get_sectors():
    return ["CTI Geral", "UCO"]

def get_patients_by_sector(sector):
    return [p for p in get_mock_patients() if p['setor'] == sector]

def get_patient_by_id(patient_id):
    for p in get_mock_patients():
        if p['id'] == patient_id:
            return p
    return None
