// src/components/ClaimsList.js
import React from 'react';

function ClaimsList({ claims }) {
    return (
        <div>
            {claims.map((claim) => (
                <div key={claim.claim._id}>
                    <img src={`uploads/${claim.claim.filename}`}  alt={claim.claim.caption} width={100} />
                    <p>{claim.claim.caption}</p>
                </div>
            ))}
        </div>
    );
}

export default ClaimsList;
