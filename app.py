# EEG Streamlit App by Muhaimin Sarker

import streamlit as st
# Load up the loader.py file
import loader 
import mne
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

# Configure page
st.set_page_config(
    layout="wide",
    page_title="EEG Motor Imagery Analysis",
    # Searched this from online 
    page_icon="🧠"
)

# Custom CSS
st.markdown("""
<style>
    .header-style {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .plot-container {
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True) # This allows for the html to be RENDERED rather than just displayed as text

# App title and description
st.title("🧠 EEG Motor Movement/Imagery Analysis")

# Wrote some markdown which helps give some background for it  
st.markdown("""
**Visualizing motor cortex activity across multiple subjects and experimental runs**  
*Data from PhysioNet EEG Motor Movement/Imagery Dataset*
""")

# Sidebar controls
with st.sidebar:
    st.header("Data Selection")
    
    # Essentially, this gets the subject ID which defaults to 1 and the increaser goes by 1 
    # Number input can be edited though
    subject = st.number_input("Subject ID", 1, 3, 1)
    st.caption("Demo includes 3 of 109 subjects")

    run = st.selectbox(
        "Experimental Run", 
        list(range(1, 15)),
        format_func=lambda x: f"Run {x}: {loader.get_run_description(x)}"
    )
    
    st.markdown("---")
    st.header("Display Options")
    # The check boxes are used to showcase different aspects of the data
    show_sensors = st.checkbox("Show sensor locations", True)
    show_psd = st.checkbox("Show power spectrum", True)
    show_all_channels = st.checkbox("Show all channels", False)
    compare_mode = st.checkbox("Enable comparison view", False)
    
    # If the compare mode is shown then just create another select box where I select the run to compare it to
    if compare_mode:
        compare_run = st.selectbox(
            "Compare with Run",
            list(range(1, 15)),
            index=1,
            format_func=lambda x: f"Run {x}: {loader.get_run_description(x)}"
        )


def create_comparison_plot(epochs1, epochs2, label1, label2):
    """Create comparison plot between two conditions with custom colors."""
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Compute the average of both epochs (these are selected in the select box pane)
    evoked1 = epochs1.average()
    evoked2 = epochs2.average()
    
    color1 = 'blue'
    color2 = 'red'
    
    # Plot motor cortex channels for epochs1 (condition 1)
    for ch, color in zip(['C3', 'C4', 'Cz'], [color1, color1, color1]):
        if ch in evoked1.info['ch_names']:
            times = evoked1.times
            data = evoked1.get_data(picks=ch)[0] 
            ax.plot(times, data, color=color, label=f"{label1} - {ch}")
    
    # Plot motor cortex channels for epochs2 (condition 2)
    for ch, color in zip(['C3', 'C4', 'Cz'], [color2, color2, color2]):
        if ch in evoked2.info['ch_names']:
            times = evoked2.times
            data = evoked2.get_data(picks=ch)[0]  
            ax.plot(times, data, color=color, label=f"{label2} - {ch}")
    
    # Add title and legend
    ax.set_title(f"Comparison: {label1} (blue) vs {label2} (red)")
    ax.legend()

    return fig



@st.cache_resource(show_spinner="Loading EEG data...")
def load_data(subject, run):
    return loader.load_subject_data(subject, run)

# Load data
try:
    epochs, event_id, error = load_data(subject, run)
    
    if error:
        st.error(error)
    elif epochs:
        # Dynamic event selection based on available events
        available_events = list(event_id.values())
        event_type = available_events[0] if available_events else "baseline"
        
        if len(available_events) > 1:
            event_type = st.sidebar.radio("Event Type", available_events)
        
        # Convert event name to ID
        event_id = [k for k, v in event_id.items() if v == event_type][0]
        
        # Main columns layout and you define how much each column should take up
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Time-Series Analysis")
            
            # Enhanced plot with more information overall
            fig, ax = plt.subplots(figsize=(12, 4))
            picks = epochs.ch_names if show_all_channels else ['C3', 'C4', 'Cz']
            
            # Highlight motor cortex in the plot using MNE and showcase the channel names
            epochs[event_id].average().plot(
                axes=ax,
                picks=picks,
                spatial_colors=True,
                gfp=True
            )

            # Set the title of this time series plot with a run descriptor
            ax.set_title(f"Subject {subject} - {loader.get_run_description(run)}\n", pad=15)
            
            # Add informative annotations to the graph 
            if run > 2:  
                task_type = loader.get_task_type(run)
                # Add this annotation to the graph upon getting the task type 
                ax.annotate(f"Task Type: {task_type.replace('_', ' ')}",
                           xy=(0.5, 1.05), xycoords='axes fraction',
                           ha='center', fontsize=10)
            
            st.pyplot(fig)
            
            # Power spectral density plot
            if show_psd:
                with st.expander("Power Spectral Density (Mu/Beta Rhythms)", expanded=True):
                    fig_psd, ax = plt.subplots(figsize=(10, 3))
                    ax.set_xlim(8, 30)
                    epochs[event_id].compute_psd().plot(
                        axes=ax,
                        picks=['C3', 'C4'],
                        average=False,
                        amplitude=False,
                    )
                    ax.set_title("Motor Cortex Power Spectrum (C3/C4)", pad=15)
                    st.pyplot(fig_psd)
            
            # Comparison view
            if compare_mode:
                epochs_compare, _, _ = load_data(subject, compare_run)
                if epochs_compare:
                    st.markdown("### Comparison View")
                    fig_compare = create_comparison_plot(
                        epochs[event_id], 
                        epochs_compare[list(epochs_compare.event_id.keys())[0]],
                        f"Run {run}",
                        f"Run {compare_run}"
                    )
                    st.pyplot(fig_compare)
        
        with col2:
            # Added some information about the session details
            st.markdown("### Session Details")
            
            # Get the run description along with some of the other meta details 
            st.markdown(f"""
            <div class="info-box">
                <div class="header-style">Subject {subject} - Run {run}</div>
                <p>{loader.get_run_description(run)}</p>
                <p><b>Condition:</b> {event_type}</p>
                <p><b>Task Type:</b> {loader.get_task_type(run).replace('_', ' ')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics cards
            col_metrics = st.columns(2)

            # With the two columns, I showcase some metadata that can be obtained from the epochs data
            with col_metrics[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Sampling Rate</h4>
                    <h2>{int(epochs.info['sfreq'])} Hz</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Events</h4>
                    <h2>{len(epochs[event_id])}</h2>
                </div>
                """, unsafe_allow_html=True)

            # I put it into the two columns to make it look more aesthetically pleasing
            with col_metrics[1]:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Channels</h4>
                    <h2>{len(epochs.ch_names)}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Duration</h4>
                    <h2>{epochs.times[-1]-epochs.times[0]:.1f}s</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional information for baseline vs task runs
            if run in [1, 2]:
                st.markdown("""
                <div class="info-box">
                    <b>Baseline Run Notes:</b>
                    <ul>
                        <li>No specific motor tasks performed</li>
                        <li>Useful for comparing resting state activity</li>
                        <li>Run 1: Eyes open, Run 2: Eyes closed</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-box">
                    <b>Task Run Notes:</b>
                    <ul>
                        <li>Task type: {loader.get_task_type(run).replace('_', ' ')}</li>
                        <li>Actual movements show stronger signals than imagined</li>
                        <li>Compare with other runs of same type (e.g., runs 3,7,11)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    # Error handling such that if I don't find any data for the subject, it'll show that warning rather than break fully
    else:
        st.warning(f"No data found for Subject {subject}, Run {run}")

except Exception as e:
    st.error(f"Error processing data: {str(e)}")

    # In general, show this as a protocol for people using the program 
    st.info("""
    Troubleshooting tips:
    1. Verify the data files exist in the correct location
    2. Check the EDF files are not corrupted
    3. Try a different subject or run
    """)