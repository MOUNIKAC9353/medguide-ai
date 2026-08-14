/* ============================================================
   MEDIASSIST - FRONTEND JAVASCRIPT
   Ballari Medical Assistant
   ============================================================ */


/* ============================================================
   GLOBAL STATE
   ============================================================ */

let currentHospitalFilter = "";
let hospitalsLoaded = false;


/* ============================================================
   SECTION NAVIGATION
   ============================================================ */

function showSection(section) {

    const sections =
        document.querySelectorAll(".section");

    sections.forEach(function (item) {
        item.classList.remove("active-section");
    });


    const target =
        document.getElementById(section + "-section");

    if (target) {
        target.classList.add("active-section");
    }


    const navItems =
        document.querySelectorAll(".nav-item");

    navItems.forEach(function (item) {
        item.classList.remove("active");
    });


    /*
     * We don't rely only on fixed indexes because
     * different versions of index.html may contain
     * slightly different navigation structures.
     */

    navItems.forEach(function (item) {

        const text =
            item.textContent.toLowerCase();

        if (
            (section === "chat" &&
                text.includes("chat")) ||

            (section === "hospitals" &&
                text.includes("hospital")) ||

            (section === "specialties" &&
                (
                    text.includes("feature") ||
                    text.includes("special")
                )) ||

            (section === "emergency" &&
                text.includes("emergency"))
        ) {
            item.classList.add("active");
        }
    });


    /*
     * Load hospital information only when required.
     */

    if (section === "hospitals") {
        loadHospitals();
    }
}


/* ============================================================
   TIME
   ============================================================ */

function getCurrentTime() {

    const now = new Date();

    return now.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}


/* ============================================================
   HTML ESCAPE
   ============================================================ */

function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* ============================================================
   USER MESSAGE
   ============================================================ */

function addUserMessage(text) {

    const container =
        document.getElementById("chatMessages");

    if (!container) {
        return;
    }


    const message =
        document.createElement("div");

    message.className = "message user";


    message.innerHTML = `
        <div class="message-content">

            <div class="message-bubble">
                ${escapeHtml(text)}
            </div>

            <span class="message-time">
                ${getCurrentTime()}
            </span>

        </div>
    `;


    container.appendChild(message);

    container.scrollTop =
        container.scrollHeight;
}


/* ============================================================
   BOT MESSAGE
   ============================================================ */

function addBotMessage(html) {

    const container =
        document.getElementById("chatMessages");

    if (!container) {
        return;
    }


    const message =
        document.createElement("div");

    message.className = "message bot";


    message.innerHTML = `
        <div class="message-avatar">
            +
        </div>

        <div class="message-content">

            <div class="message-bubble">
                ${html}
            </div>

            <span class="message-time">
                ${getCurrentTime()}
            </span>

        </div>
    `;


    container.appendChild(message);

    container.scrollTop =
        container.scrollHeight;
}


/* ============================================================
   TYPING INDICATOR
   ============================================================ */

function showTyping() {

    removeTyping();


    const container =
        document.getElementById("chatMessages");

    if (!container) {
        return;
    }


    const typing =
        document.createElement("div");

    typing.id =
        "typingIndicator";

    typing.className =
        "message bot";


    typing.innerHTML = `
        <div class="message-avatar">
            +
        </div>

        <div class="message-content">

            <div class="message-bubble">
                🤖 MediAssist is processing...
            </div>

        </div>
    `;


    container.appendChild(typing);

    container.scrollTop =
        container.scrollHeight;
}


function removeTyping() {

    const typing =
        document.getElementById(
            "typingIndicator"
        );

    if (typing) {
        typing.remove();
    }
}


/* ============================================================
   CHAT
   ============================================================ */

async function sendMessage() {

    const input =
        document.getElementById(
            "messageInput"
        );

    if (!input) {
        return;
    }


    const text =
        input.value.trim();


    if (!text) {
        return;
    }


    addUserMessage(text);

    input.value = "";

    showTyping();


    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: text
                    })
                }
            );


        const data =
            await response.json();


        removeTyping();


        if (!response.ok) {

            addBotMessage(`
                <div class="error-message">

                    <strong>
                        ⚠️ Unable to process request
                    </strong>

                    <p>
                        ${escapeHtml(
                            data.message ||
                            "Please try again."
                        )}
                    </p>

                </div>
            `);

            return;
        }


        renderChatResponse(data);

    }

    catch (error) {

        removeTyping();

        console.error(
            "Chat error:",
            error
        );


        addBotMessage(`
            <div class="error-message">

                <strong>
                    ⚠️ Connection problem
                </strong>

                <p>
                    Unable to connect to the
                    MediAssist backend.
                </p>

                <p>
                    Please make sure Flask is running.
                </p>

            </div>
        `);
    }
}


/* ============================================================
   RENDER CHAT RESPONSE
   ============================================================ */

function renderChatResponse(data) {

    let html = "";


    /* --------------------------------------------------------
       EMERGENCY
       -------------------------------------------------------- */

    if (data.emergency) {

        html += `
            <div class="emergency-response">

                <h3>
                    🚨 Urgent Situation
                </h3>

                <p>
                    ${escapeHtml(
                        data.message ||
                        "This may require immediate medical attention."
                    )}
                </p>

                ${
                    data.action
                    ?
                    `
                    <p>
                        <strong>
                            What to do:
                        </strong>
                        ${escapeHtml(data.action)}
                    </p>
                    `
                    :
                    ""
                }

            </div>
        `;


        if (
            data.hospitals &&
            data.hospitals.length > 0
        ) {

            html += `
                <hr>

                <h4>
                    🏥 Nearby/Available Emergency Facilities
                </h4>

                <div class="chat-hospital-list">
            `;


            data.hospitals.forEach(
                function (hospital) {

                    html +=
                        createChatHospitalCard(
                            hospital
                        );
                }
            );


            html += `
                </div>
            `;
        }


        addBotMessage(html);

        return;
    }


    /* --------------------------------------------------------
       NORMAL MESSAGE
       -------------------------------------------------------- */

    if (data.message) {

        html += `
            <p>
                ${escapeHtml(data.message)}
            </p>
        `;
    }


    /* --------------------------------------------------------
       INTENT
       -------------------------------------------------------- */

    if (data.intent) {

        html += `
            <div class="response-info">

                <strong>
                    🧠 Detected request:
                </strong>

                ${escapeHtml(data.intent)}

            </div>
        `;
    }


    /* --------------------------------------------------------
       SYMPTOM
       -------------------------------------------------------- */

    if (data.symptom) {

        html += `
            <div class="symptom-result">

                <hr>

                <p>
                    🩺
                    <strong>
                        Symptom:
                    </strong>

                    ${escapeHtml(data.symptom)}
                </p>

                <p>
                    👨‍⚕️
                    <strong>
                        Suggested specialist:
                    </strong>

                    ${escapeHtml(
                        data.specialty ||
                        "General Medicine"
                    )}
                </p>

                ${
                    data.guidance
                    ?
                    `
                    <p>
                        ${escapeHtml(data.guidance)}
                    </p>
                    `
                    :
                    ""
                }

            </div>
        `;
    }


    /* --------------------------------------------------------
       SPECIALTY
       -------------------------------------------------------- */

    if (data.specialty && !data.symptom) {

        html += `
            <p>
                👨‍⚕️
                <strong>
                    Specialty:
                </strong>

                ${escapeHtml(data.specialty)}
            </p>
        `;
    }


    /* --------------------------------------------------------
       CONDITION
       -------------------------------------------------------- */

    if (data.condition) {

        html += `
            <div class="condition-result">

                <p>
                    🔎
                    <strong>
                        Possible condition category:
                    </strong>

                    ${escapeHtml(data.condition)}
                </p>

                <small>
                    This is educational information,
                    not a confirmed diagnosis.
                </small>

            </div>
        `;
    }


    /* --------------------------------------------------------
       HOSPITALS
       -------------------------------------------------------- */

    if (
        data.hospitals &&
        data.hospitals.length > 0
    ) {

        html += `
            <hr>

            <h4>
                🏥 Recommended Healthcare Facilities
            </h4>

            <div class="chat-hospital-list">
        `;


        data.hospitals.forEach(
            function (hospital) {

                html +=
                    createChatHospitalCard(
                        hospital
                    );
            }
        );


        html += `
            </div>
        `;
    }


    /* --------------------------------------------------------
       FALLBACK
       -------------------------------------------------------- */

    if (!html.trim()) {

        html = `
            <p>
                ${escapeHtml(
                    data.message ||
                    "I could not generate a response."
                )}
            </p>
        `;
    }


    addBotMessage(html);
}


/* ============================================================
   CHAT HOSPITAL CARD
   ============================================================ */

function createChatHospitalCard(hospital) {

    if (!hospital) {
        return "";
    }


    const website =
        hospital.website || "";


    let websiteHTML = "";


    if (website) {

        websiteHTML = `
            <a
                href="${escapeHtml(website)}"
                target="_blank"
                rel="noopener noreferrer"
                class="hospital-link"
            >
                🌐 Hospital Website
            </a>
        `;
    }


    return `
        <div class="chat-hospital-card">

            <div class="chat-hospital-icon">
                🏥
            </div>

            <div class="chat-hospital-content">

                <h4>
                    ${escapeHtml(
                        hospital.name
                    )}
                </h4>

                ${
                    hospital.hospital_type
                    ?
                    `
                    <span class="hospital-type">
                        ${escapeHtml(
                            hospital.hospital_type
                        )}
                    </span>
                    `
                    :
                    ""
                }

                ${
                    hospital.address
                    ?
                    `
                    <p>
                        📍
                        ${escapeHtml(
                            hospital.address
                        )}
                    </p>
                    `
                    :
                    ""
                }

                ${
                    hospital.phone
                    ?
                    `
                    <p>
                        📞
                        ${escapeHtml(
                            hospital.phone
                        )}
                    </p>
                    `
                    :
                    ""
                }

                ${
                    hospital.hospital_timings
                    ?
                    `
                    <p>
                        🕒
                        ${escapeHtml(
                            hospital.hospital_timings
                        )}
                    </p>
                    `
                    :
                    ""
                }

                ${
                    hospital.emergency_phone
                    ?
                    `
                    <p>
                        🚑 Emergency:
                        ${escapeHtml(
                            hospital.emergency_phone
                        )}
                    </p>
                    `
                    :
                    ""
                }

                ${websiteHTML}

            </div>

        </div>
    `;
}


/* ============================================================
   QUICK MESSAGE
   ============================================================ */

function sendQuickMessage(text) {

    const input =
        document.getElementById(
            "messageInput"
        );

    if (!input) {
        return;
    }


    input.value = text;

    sendMessage();
}


/* ============================================================
   LOAD ALL HOSPITALS
   ============================================================ */

async function loadHospitals() {

    const container =
        document.getElementById(
            "hospitalContainer"
        );


    if (!container) {
        return;
    }


    currentHospitalFilter = "";


    container.innerHTML = `
        <div class="loading-card">
            🏥 Loading Ballari healthcare facilities...
        </div>
    `;


    try {

        const response =
            await fetch(
                "/api/hospitals"
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Hospital request failed."
            );
        }


        hospitalsLoaded = true;


        renderHospitals(
            data.hospitals || [],
            container
        );

    }

    catch (error) {

        console.error(
            "Hospital loading error:",
            error
        );


        container.innerHTML = `
            <div class="loading-card">

                <h3>
                    ⚠️ Unable to load hospitals
                </h3>

                <p>
                    Please make sure the Flask
                    backend and database are running.
                </p>

            </div>
        `;
    }
}


/* ============================================================
   RENDER HOSPITALS
   ============================================================ */

function renderHospitals(
    hospitals,
    container
) {

    container.innerHTML = "";


    if (
        !hospitals ||
        hospitals.length === 0
    ) {

        container.innerHTML = `
            <div class="loading-card">

                <h3>
                    🏥 No hospitals found
                </h3>

                <p>
                    No healthcare facilities are
                    currently available for this search.
                </p>

            </div>
        `;

        return;
    }


    hospitals.forEach(
        function (hospital) {

            container.appendChild(
                createHospitalCard(
                    hospital
                )
            );
        }
    );
}


/* ============================================================
   HOSPITAL CARD
   ============================================================ */

function createHospitalCard(hospital) {

    const card =
        document.createElement("div");


    card.className =
        "hospital-card";


    let doctorsHTML = "";


    if (
        hospital.doctors &&
        hospital.doctors.length > 0
    ) {

        doctorsHTML = `
            <div class="doctors-section">

                <h4>
                    👨‍⚕️ Available Doctors
                </h4>
        `;


        hospital.doctors.forEach(
            function (doctor) {

                doctorsHTML += `
                    <div class="doctor-box">

                        <strong>
                            ${escapeHtml(
                                doctor.doctor_name
                            )}
                        </strong>

                        <p>
                            🩺
                            ${escapeHtml(
                                doctor.specialty ||
                                "General"
                            )}
                        </p>

                        ${
                            doctor.qualification
                            ?
                            `
                            <p>
                                🎓
                                ${escapeHtml(
                                    doctor.qualification
                                )}
                            </p>
                            `
                            :
                            ""
                        }

                        ${
                            doctor.opd_days
                            ?
                            `
                            <p>
                                📅
                                ${escapeHtml(
                                    doctor.opd_days
                                )}
                            </p>
                            `
                            :
                            ""
                        }

                        ${
                            doctor.opd_start_time
                            ?
                            `
                            <p>
                                🕒
                                ${escapeHtml(
                                    doctor.opd_start_time
                                )}
                                -
                                ${escapeHtml(
                                    doctor.opd_end_time ||
                                    ""
                                )}
                            </p>
                            `
                            :
                            ""
                        }

                        ${
                            doctor.appointment_phone
                            ?
                            `
                            <p>
                                📞
                                ${escapeHtml(
                                    doctor.appointment_phone
                                )}
                            </p>
                            `
                            :
                            ""
                        }

                        ${
                            doctor.availability_status
                            ?
                            `
                            <span class="doctor-status">
                                ${escapeHtml(
                                    doctor.availability_status
                                )}
                            </span>
                            `
                            :
                            ""
                        }

                    </div>
                `;
            }
        );


        doctorsHTML += `
            </div>
        `;

    } else {

        doctorsHTML = `
            <div class="doctors-section">

                <h4>
                    👨‍⚕️ Doctor Information
                </h4>

                <p>
                    Doctor information is not
                    currently available.
                </p>

            </div>
        `;
    }


    let websiteHTML = "";


    if (hospital.website) {

        websiteHTML = `
            <a
                href="${escapeHtml(
                    hospital.website
                )}"
                target="_blank"
                rel="noopener noreferrer"
                class="hospital-link"
            >
                🌐 Visit Website
            </a>
        `;
    }


    card.innerHTML = `

        <div class="hospital-icon">
            🏥
        </div>

        <h3>
            ${escapeHtml(
                hospital.name
            )}
        </h3>

        ${
            hospital.hospital_type
            ?
            `
            <span class="hospital-type">
                ${escapeHtml(
                    hospital.hospital_type
                )}
            </span>
            `
            :
            ""
        }


        <div class="hospital-info">

            ${
                hospital.specialties
                ?
                `
                <div>
                    <strong>
                        🩺 Specialties
                    </strong>

                    <br>

                    ${escapeHtml(
                        hospital.specialties
                    )}
                </div>
                `
                :
                ""
            }


            ${
                hospital.address
                ?
                `
                <div>
                    <strong>
                        📍 Address
                    </strong>

                    <br>

                    ${escapeHtml(
                        hospital.address
                    )}
                </div>
                `
                :
                ""
            }


            ${
                hospital.phone
                ?
                `
                <div class="hospital-phone">
                    📞
                    ${escapeHtml(
                        hospital.phone
                    )}
                </div>
                `
                :
                ""
            }


            ${
                hospital.emergency_phone
                ?
                `
                <div>
                    <strong>
                        🚑 Emergency
                    </strong>

                    <br>

                    ${escapeHtml(
                        hospital.emergency_phone
                    )}
                </div>
                `
                :
                ""
            }


            ${
                hospital.hospital_timings
                ?
                `
                <div>
                    <strong>
                        🕒 Timings
                    </strong>

                    <br>

                    ${escapeHtml(
                        hospital.hospital_timings
                    )}
                </div>
                `
                :
                ""
            }


            ${
                hospital.services_detail
                ?
                `
                <div>
                    <strong>
                        ⚕️ Services
                    </strong>

                    <br>

                    ${escapeHtml(
                        hospital.services_detail
                    )}
                </div>
                `
                :
                ""
            }

        </div>


        ${
            hospital.emergency_available
            ?
            `
            <span class="emergency-badge">
                🚑
                ${escapeHtml(
                    hospital.emergency_available
                )}
            </span>
            `
            :
            ""
        }


        <div class="hospital-actions">

            ${
                hospital.phone
                ?
                `
                <a
                    href="tel:${escapeHtml(
                        hospital.phone
                    )}"
                    class="hospital-action-button"
                >
                    📞 Call
                </a>
                `
                :
                ""
            }

            ${websiteHTML}

        </div>


        ${doctorsHTML}

    `;


    return card;
}


/* ============================================================
   SPECIALTY SEARCH
   ============================================================ */

async function searchSpecialty(
    specialty
) {

    if (!specialty) {
        return;
    }


    currentHospitalFilter =
        specialty;


    showSection("hospitals");


    const container =
        document.getElementById(
            "hospitalContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = `
        <div class="loading-card">

            🔎 Searching for
            <strong>
                ${escapeHtml(specialty)}
            </strong>
            hospitals...

        </div>
    `;


    try {

        const response =
            await fetch(
                "/api/hospitals?specialty=" +
                encodeURIComponent(
                    specialty
                )
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Specialty search failed."
            );
        }


        renderHospitals(
            data.hospitals || [],
            container
        );


    }

    catch (error) {

        console.error(
            "Specialty search error:",
            error
        );


        container.innerHTML = `
            <div class="loading-card">

                <h3>
                    ⚠️ Search failed
                </h3>

                <p>
                    Unable to find
                    ${escapeHtml(specialty)}
                    hospitals.
                </p>

            </div>
        `;
    }
}


/* ============================================================
   SPECIALTY BUTTON HELPERS
   ============================================================ */

function showSkinHospitals() {

    searchSpecialty(
        "Dermatology"
    );
}


function showEyeHospitals() {

    searchSpecialty(
        "Ophthalmology"
    );
}


function showHeartHospitals() {

    searchSpecialty(
        "Cardiology"
    );
}


function showFeverInformation() {

    /*
     * Fever is generally handled through
     * General Medicine.
     *
     * We intentionally do NOT prescribe
     * medication automatically.
     */

    const input =
        document.getElementById(
            "messageInput"
        );


    if (input) {

        input.value =
            "I have fever. What general care should I take and when should I see a doctor?";

        sendMessage();

    } else {

        showSection("chat");

    }
}


/* ============================================================
   FEATURE / SPECIALTY QUICK ACTIONS
   ============================================================ */

function handleFeature(feature) {

    const normalized =
        String(feature || "")
            .toLowerCase();


    if (
        normalized.includes("skin") ||
        normalized.includes("dermat")
    ) {

        searchSpecialty(
            "Dermatology"
        );

        return;
    }


    if (
        normalized.includes("eye") ||
        normalized.includes("vision") ||
        normalized.includes("ophthalm")
    ) {

        searchSpecialty(
            "Ophthalmology"
        );

        return;
    }


    if (
        normalized.includes("heart") ||
        normalized.includes("cardio")
    ) {

        searchSpecialty(
            "Cardiology"
        );

        return;
    }


    if (
        normalized.includes("fever")
    ) {

        showFeverInformation();

        return;
    }
}


/* ============================================================
   HOSPITAL SEARCH FROM SEARCH INPUT
   ============================================================ */

async function filterHospitalsFromInput() {

    const input =
        document.getElementById(
            "hospitalSearch"
        );


    if (!input) {
        return;
    }


    const value =
        input.value.trim();


    if (!value) {

        loadHospitals();

        return;
    }


    /*
     * Send the search term to backend
     * as a specialty search.
     */

    await searchSpecialty(
        value
    );
}


/* ============================================================
   CLEAR HOSPITAL FILTER
   ============================================================ */

function clearHospitalFilter() {

    currentHospitalFilter = "";

    loadHospitals();
}


/* ============================================================
   BACKEND STATUS
   ============================================================ */

async function checkBackendStatus() {

    try {

        const response =
            await fetch(
                "/api/status"
            );


        const data =
            await response.json();


        console.log(
            "MediAssist backend status:",
            data
        );


        if (!data.models_loaded) {

            console.warn(
                "⚠️ ML models are not loaded."
            );
        }


        if (!data.database_available) {

            console.warn(
                "⚠️ Hospital database is not available."
            );
        }


    }

    catch (error) {

        console.error(
            "Backend status check failed:",
            error
        );
    }
}


/* ============================================================
   ENTER KEY
   ============================================================ */

function setupMessageInput() {

    const input =
        document.getElementById(
            "messageInput"
        );


    if (!input) {
        return;
    }


    input.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();
            }

        }
    );
}


/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        setupMessageInput();

        checkBackendStatus();

        console.log(
            "🏥 MediAssist frontend initialized."
        );

    }
);